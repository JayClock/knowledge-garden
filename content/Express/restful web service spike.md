---
date: 2025-04-10T22:01:23
updated: 2025-04-12T20:39:33
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
    const rootResource = [...this.application.getClasses().values()].filter(c => {
      return Reflect.hasMetadata(PATH_METADATA, c);
    })[0];
    const instance: any = new rootResource();
    const methods = Object.getOwnPropertyNames(rootResource.prototype)
      .filter(key => Reflect.hasMetadata(HTTP_METHOD_METADATA, instance, key))
      .filter(key => {
        const httpMethod = Reflect.getMetadata(HTTP_METHOD_METADATA, instance, key);
        const endPath = Reflect.getMetadata(PATH_METADATA, instance, key);
        return req.method === httpMethod && req.path.endsWith(endPath);
      });
    const result = await instance[methods[0]]();
    res.send(result);
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
  private application: TestApplication;

  constructor(application: TestApplication) {
    this.application = application;
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
    const methodKey = methods[0];
    return await instance[methodKey]();
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


```ts
import express, { Express, Request, Response } from 'express';
import { Server } from 'node:http';
import supertest from 'supertest';
import { Get, HTTP_METHOD_METADATA, Path, PATH_METADATA, Provider, PROVIDER_METADATA } from './decorators';
import { BodyWriter, Class } from './core';

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
  private application: TestApplication;

  constructor(application: TestApplication) {
    this.application = application;
  }

  async handle(req: Request, res: Response) {
    const rootResources = [...this.application.getClasses().values()].filter(c => {
      return Reflect.hasMetadata(PATH_METADATA, c);
    });
    const writers = [...this.application.getClasses().values()].filter(c => {
      return Reflect.hasMetadata(PROVIDER_METADATA, c);
    });

    const writer: BodyWriter<string> = new writers[0]();

    const result = await this.dispatch(req, rootResources);
    writer.write(result, res);
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
    const methodKey = methods[0];
    return await instance[methodKey]();
  }
}

class TestApplication {
  getClasses(): Set<Class> {
    return new Set([UserResource, StringMessageBodyWriter]);
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
    return true;
  }

  write(data: string, res: Response): void {
    res.send(data);
  }
}

```
