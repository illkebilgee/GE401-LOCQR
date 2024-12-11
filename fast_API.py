from fastapi import FastAPI, Form
from fastapi.responses import StreamingResponse, HTMLResponse
import qrcode
from io import BytesIO
import os

app = FastAPI()

active_sessions = {}

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

@app.get("/")
async def home():
    html_content = """
    <html>
        <head><title>QR Code Login</title></head>
        <body>
            <h1>Scan the QR Code to Login</h1>
            <img src="/generate_qr?session_id=12345" alt="QR Code">
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/generate_qr")
async def generate_qr(session_id: str):
    public_url = "https://your-app-name.onrender.com"
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(f"{public_url}/authenticate?session_id={session_id}")
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="image/png")

"""
@app.get("/generate_qr")
async def generate_qr(session_id: str):
    # Use your actual Render public URL
    public_url = "https://your-app-name.onrender.com"
    
    # Generate the QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(f"{public_url}/authenticate?session_id={session_id}")
    qr.make(fit=True)

    # Convert to PNG image
    img = qr.make_image(fill="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return StreamingResponse(buffer, media_type="image/png")
    """


@app.get("/authenticate")
async def authenticate(session_id: str):
    
    if session_id not in active_sessions:
        active_sessions[session_id] = "authenticated"
        return HTMLResponse(content="""
        <html>
            <head><title>Login</title></head>
            <body>
                <h1>Login with UserID and Password</h1>
                <form action="/login" method="post">
                    <label for="user_id">UserID:</label><br>
                    <input type="text" id="user_id" name="user_id"><br><br>
                    <label for="password">Password:</label><br>
                    <input type="password" id="password" name="password"><br><br>
                    <input type="submit" value="Login">
                </form>
            </body>
        </html>
        """)
    return {"message": "Session already authenticated!"}

@app.post("/login")
async def login(user_id: str = Form(...), password: str = Form(...)):
    if user_id == "admin" and password == "password":
        return {"message": "Login successful!"}
    else:
        return {"message": "Invalid UserID or Password!"}
        
import os

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # Default to 8000 if PORT is not set
    uvicorn.run("fast_API:app", host="0.0.0.0", port=port)


#bu kod qr üreten bir siteye gidiyor o qr da başka bir siteye yönlendiriyor
# from fastapi import FastAPI, WebSocket
# import qrcode
# from io import BytesIO
# from fastapi.responses import StreamingResponse, HTMLResponse

# #cd /Users/ilkebilgeyevgi/Desktop
# #uvicorn fast_API:app --reload

# app = FastAPI()

# active_sessions = {}

# @app.get("/")
# async def home():
#     html_content = """
#     <html>
#         <head><title>QR Code Login</title></head>
#         <body>
#             <h1>Scan the QR Code to Login</h1>
#             <img src="/generate_qr?session_id=12345" alt="QR Code">
#         </body>
#     </html>
#     """
#     return HTMLResponse(content=html_content)

# @app.get("/generate_qr")
# async def generate_qr(session_id: str):
#     qr = qrcode.QRCode(version=1, box_size=10, border=4)
#     qr.add_data(f"http://127.0.0.1:8000/authenticate?session_id={session_id}")
#     qr.make(fit=True)

#     img = qr.make_image(fill="black", back_color="white")
#     buffer = BytesIO()
#     img.save(buffer, format="PNG")
#     buffer.seek(0)
#     return StreamingResponse(buffer, media_type="image/png")

# @app.get("/authenticate")
# async def authenticate(session_id: str):
#     if session_id not in active_sessions:
#         active_sessions[session_id] = "authenticated"
#         return {"message": "Authenticated successfully!"}
#     return {"message": "Session already authenticated!"}

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         for session, status in active_sessions.items():
#             if status == "authenticated":
#                 await websocket.send_text(f"Session {session} authenticated!")
#                 active_sessions.pop(session)
#                 break
#         await websocket.receive_text()
