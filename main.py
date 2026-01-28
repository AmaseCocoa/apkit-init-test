import uvicorn

import app

uvicorn.run(app.app, port=8081)