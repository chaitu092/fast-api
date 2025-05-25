1. Install vscode
2. Create virtual envirnoment
    python -m venv {your env name}myvenv
3. Activate virtual environment
    mac- source myenv/bin/activate
    windows - myenv\Scripts\activate
![alt text](image.png)

4. Install dependencies
    pip install fastapi uvicorn pydantic

5. Start build your APIs/endpoints 🙈

6. Command to run - uvicorn {filename}hello_api:app --reload

7. Troubleshooting - ![port error](image.png)

when you came accross such error.

Terminate the existing process using the port

Step-1
Find process id using port
lsof -i:8000

this will list the processes using port `8000`. Example the output shown below:
![alt text](image-1.png)

Step - 2
kill the process

kill -9 <PID>
for example

kill -9 30006