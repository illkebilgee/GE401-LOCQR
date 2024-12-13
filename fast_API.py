from fastapi import FastAPI, Form
from fastapi.responses import StreamingResponse, HTMLResponse
import qrcode
from io import BytesIO
import os

# Create the FastAPI application
app = FastAPI()

# Store active sessions
active_sessions = {}

# Get the public URL from the environment or use a default value
public_url = os.getenv("PUBLIC_URL", "https://your-app-name.onrender.com")

@app.get("/")
async def home():
    html_content = f"""
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
    # Generate the QR code URL
    qr_url = f"{public_url}/authenticate?session_id={session_id}"
    
    # Create the QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(qr_url)
    qr.make(fit=True)

    # Convert the QR code to a PNG image
    img = qr.make_image(fill="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # Return the QR code image as a response
    return StreamingResponse(buffer, media_type="image/png")

@app.get("/authenticate")
async def authenticate(session_id: str):
    # Check if the session ID exists
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
    # Validate login credentials
    if user_id == "admin" and password == "password":
        return {"message": "Login successful!"}
    else:
        return {"message": "Invalid UserID or Password!"}

if __name__ == "__main__":
    import uvicorn
    # Get the port from the environment variable or use 8000 by default
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("qr_code_login:app", host="0.0.0.0", port=port)
