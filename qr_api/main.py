from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import qrcode
from io import BytesIO

app = FastAPI()

class QRRequest(BaseModel):
    merchant_id: str
    valor: str

@app.post("/gerar_qr")
def gerar_qr(data: QRRequest):
    try:
        ussd_code = f"*475*{data.merchant_id}*{data.valor}#"
        qr = qrcode.QRCode(box_size=10, border=4)
        qr.add_data(ussd_code)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        buf = BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)

        return StreamingResponse(buf, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
