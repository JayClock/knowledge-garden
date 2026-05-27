---
date: 2025-04-10T22:01:23
updated: 2026-05-15 10:03:23
share: true
---
首先，我们构造一个最简单的测试用例，仅仅是请求 `/users`，并返回 'user list'

```ts
import express, { Express } from 'express';
import { Server } from 'node:http';
import supertest from 'supertest';

describe('ResourceServlet', () => {
  let app: Express;
  let server: Server;

  beforeAll(() => {
    app = express();
    server = app.listen(3000);

    app.get('/users', (req, res) => {
      res.send('user list');
    });
  });

  afterAll(() => {
    server.close();
  });

  it('should return user list when fetch "users"', async () => {
    const response = await supertest(app).get('/users');
    expect(response.text).toBe('user list');
  });
});
```

接着，我们吧获取 `user list` 的的逻辑，封装到 UserResource.findAll 中，这样子，我们的预想的架构愿景，就变成了，拿到 @Path 装饰的类，并根据路由找到请求方法。

```ts
import express, { Express } from 'express';
import { Server } from 'node:http';
import supertest from 'supertest';
import { Get, Path } from './decorators';

describe('ResourceServlet', () => {
  let app: Express;
  let server: Server;

  beforeAll(() => {
    app = express();
    server = app.listen(3000);

    app.get('/users', async (req, res) => {
      const result = await new UserResource().findAll()
      res.send(result);
    });
  });

  afterAll(() => {
    server.close();
  });

  it('should return user list when fetch "users"', async () => {
    const response = await supertest(app).get('/users');
    expect(response.text).toBe('user list');
  });
});

@Path('/users')
class UserResource {
  @Get()
  async findAll() {
    return 'user list';
  }
}
```

添加 dispatch
```ts
import express, { Express, Request, Response } from 'express';
import { Server } from 'node:http';
import supertest from 'supertest';
import { Get, HTTP_METHOD_METADATA, Path, PATH_METADATA } from './decorators';
import { Class } from './core';

describe('ResourceServlet', () => {
  let app: Express;
  let server: Server;

  beforeAll(() => {
    app = express();
    server = app.listen(3000);

    app.get('/users', async (req, res) => {
      const application = new TestApplication();
      const servlet = new ResourceServlet(application);
      await servlet.handle(req, res);
    });
  });

  afterAll(() => {
    server.close();
  });

  it('should return user list when fetch "users"', async () => {
    const response = await supertest(app).get('/users');
    expect(response.text).toBe('user list');
  });
});

class ResourceServlet {
  constructor(private readonly application: TestApplication) {
  }

  async handle(req: Request, res: Response) {
    const rootResources = [...this.application.getClasses().values()].filter(c => {
      return Reflect.hasMetadata(PATH_METADATA, c);
    });
    const result = await this.dispatch(req, rootResources);
    res.send(result);
  }

  async dispatch(req: Request, rootResources: Class[]) {
    const rootResource = rootResources[0];
    const instance: any = new rootResource();
    const methods = Object.getOwnPropertyNames(rootResource.prototype)
      .filter(key => Reflect.hasMetadata(HTTP_METHOD_METADATA, instance, key))
      .filter(key => {
        const httpMethod = Reflect.getMetadata(HTTP_METHOD_METADATA, instance, key);
        const endPath = Reflect.getMetadata(PATH_METADATA, instance, key);
        return req.method === httpMethod && req.path.endsWith(endPath);
      });
    return await instance[methods[0]]();
  }
}

class TestApplication {
  getClasses(): Set<Class> {
    return new Set([UserResource]);
  }
}

@Path('/users')
class UserResource {
  @Get()
  async findAll() {
    return 'user list';
  }
}
```

现在我们的 res.send(result); 场景太单一了，我们现实的业务，会根据 Head 中不同的 media type，去向前端返回不同格式的数据。这里我们可以抽象一个 bodywriter

```ts
import express, { Express, Request, Response } from 'express';
import { Server } from 'node:http';
import supertest from 'supertest';
import { Get, HTTP_METHOD_METADATA, Path, PATH_METADATA, Provider, PROVIDER_METADATA } from './decorators';
import { BodyWriter, Class, OutResponse } from './core';

describe('ResourceServlet', () => {
  let app: Express;
  let server: Server;

  beforeAll(() => {
    app = express();
    server = app.listen(3000);

    app.get('/users', async (req, res) => {
      const application = new TestApplication();
      const servlet = new ResourceServlet(application);
      await servlet.handle(req, res);
    });
  });

  afterAll(() => {
    server.close();
  });

  it('should return user list when fetch "users"', async () => {
    const response = await supertest(app).get('/users');
    expect(response.text).toBe('user list');
  });
});

class ResourceServlet {
  constructor(private readonly application: TestApplication) {
  }

  async handle(req: Request, res: Response) {
    const rootResources = this.application.getClasses().filter(c => {
      return Reflect.hasMetadata(PATH_METADATA, c);
    });
    const outResponse = await this.dispatch(req, rootResources);
    const providers = new TestProviders(this.application);
    const writer = providers.getMessageBodyWriter(outResponse.mediaType);
    await writer.write(outResponse.result, res);
  }

  async dispatch(req: Request, rootResources: Class[]): Promise<OutResponse> {
    const rootResource = rootResources[0];
    const instance: any = new rootResource();
    const methodPropertyKeys = Object.getOwnPropertyNames(rootResource.prototype)
      .filter(key => Reflect.hasMetadata(HTTP_METHOD_METADATA, instance, key))
      .filter(key => {
        const httpMethod = Reflect.getMetadata(HTTP_METHOD_METADATA, instance, key);
        const endPath = Reflect.getMetadata(PATH_METADATA, instance, key);
        return req.method === httpMethod && req.path.endsWith(endPath);
      });
    const result = await instance[methodPropertyKeys[0]]();
    return new OutResponse(result, 'string');
  }
}

class TestProviders {
  constructor(private readonly application: TestApplication) {
  }

  getMessageBodyWriter<T>(mediaType: string): BodyWriter<T> {
    const writers = this.application.getClasses().filter(c => Reflect.hasMetadata(PROVIDER_METADATA, c)) as unknown as BodyWriter<any>[];
    return writers.filter(writer => new writer().canWrite(mediaType)).map(writer => new writer())[0];
  }
}

class TestApplication {
  getClasses(): Class[] {
    return [UserResource, StringMessageBodyWriter];
  }
}

@Path('/users')
class UserResource {
  @Get()
  async findAll() {
    return 'user list';
  }
}

@Provider()
class StringMessageBodyWriter implements BodyWriter<string> {
  canWrite(accept: string): boolean {
    return accept === 'string';
  }

  async write(data: string, res: Response): Promise<void> {
    res.send(data);
  }
}
```

现在我们的代码中，有些没有必要的实例创建，比如 BodyWriter 全局不管怎样，我们都应该拿到同一个实例。自然地，我们可以借助依赖注入，进行全局实例的管理。

比如在 inversify js 的帮助下，获取 body writer 可以这么做。
目前 ts 的元数据 api 和 java 比太弱了，有点难整。
```ts
class TestProviders {
  private readonly container = new Container();
  private writers: BodyWriter<any>[] = [];

  constructor(private readonly application: TestApplication) {
    const writerClasses = this.application.getClasses().filter(c => Reflect.hasMetadata(PROVIDER_METADATA, c));
    writerClasses.forEach(writerClass => {
      this.container.bind(writerClass).toSelf().inSingletonScope();
      this.writers.push(this.container.get(writerClass) as BodyWriter<any>);
    });
  }

  getMessageBodyWriter<T>(mediaType: string): BodyWriter<T> {
    return this.writers.filter(writer => writer.canWrite(mediaType))[0];
  }
}
```