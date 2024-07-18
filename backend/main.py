

from routers import routers
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(

)
origins = [
    "*",
    'http://195.135.212.242',
    'http://195.135.212.242:3000',
    'http://195.135.212.242/',
    'http://195.135.212.242:3000/'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routers.vacancies_routers)





