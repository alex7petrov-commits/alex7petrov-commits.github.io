from pathlib import Path
import base64,io,re
import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageFilter

P=Path(".")
S=(P/"index.html").read_text(encoding="utf-8")
photo64=re.search(r'<img class="portrait" src="data:image/jpeg;base64,([A-Za-z0-9+/=]+)"',S).group(1)
photo=Image.open(io.BytesIO(base64.b64decode(photo64))).convert("RGB")
qr=qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=20, border=4)
qr.add_data("https://alex7petrov-commits.github.io/")
qr.make(fit=True)
qr.make_image(fill_color="#071728",back_color="white").convert("RGB").save("qr-website.png")
W,H=1200,630
im=Image.new("RGB",(W,H))
px=im.load()
for y in range(H):
    for x in range(W):
        px[x,y]=(int(6+13*x/W+5*y/H),int(18+30*x/W+2*y/H),int(35+43*x/W+3*y/H))
d=ImageDraw.Draw(im,"RGBA")
for i,(x,h,w) in enumerate([(1000,480,130),(1110,560,130),(1170,400,60),(920,300,95)]):
    y=H-h
    d.polygon([(x,y+35),(x+42,y),(x+w,y+10),(x+w,H),(x,H)],fill=(8+8*i,21+8*i,36+8*i,200),outline=(90,122,154,130),width=2)
    for wx in range(x+16,x+w-10,24):
        for wy in range(y+60,H-15,37):
            if (wx//24+wy//37)%4!=0:
                d.rectangle((wx,wy,wx+10,wy+17),fill=(225,167,87,130))
d.polygon([(0,528),(785,630),(0,630)],fill=(2,9,20,135))
d.line((34,535,1165,535),fill=(232,177,90,220),width=3)
d.line([(52,91),(52,43),(92,20),(92,96)],fill=(237,183,97),width=5)
d.line([(92,43),(121,60),(121,96)],fill=(237,183,97),width=5)
sz=328
cx,cy=235,315
shadow=Image.new("RGBA",(W,H),(0,0,0,0))
ImageDraw.Draw(shadow).ellipse((cx-sz//2-9,cy-sz//2-9,cx+sz//2+9,cy+sz//2+9),fill=(0,0,0,140))
im=Image.alpha_composite(im.convert("RGBA"),shadow.filter(ImageFilter.GaussianBlur(16)))
face=photo.resize((sz,sz),Image.Resampling.LANCZOS)
mask=Image.new("L",(sz,sz),0)
ImageDraw.Draw(mask).ellipse((0,0,sz-1,sz-1),fill=255)
im.paste(face,(cx-sz//2,cy-sz//2),mask)
d=ImageDraw.Draw(im,"RGBA")
d.ellipse((cx-sz//2-3,cy-sz//2-3,cx+sz//2+3,cy+sz//2+3),outline=(237,187,109,255),width=6)
def f(sz,bold=False,serif=False):
    paths=["/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf","/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
    return ImageFont.truetype(paths[0 if serif else 1 if bold else 2],sz)
x=458
d.text((x,63),"НЕДВИЖИМОСТЬ  И  ПРАВО",font=f(22),fill=(231,235,241,255))
d.line((x,108,1124,108),fill=(229,180,95,220),width=2)
d.text((x,143),"Александр",font=f(68,serif=True),fill="white")
d.text((x,227),"Петров",font=f(76,serif=True),fill="white")
d.text((x,339),"РИЭЛТОР  |  ЮРИСТ",font=f(29,bold=True),fill=(226,193,126,255))
d.text((x,412),"Недвижимость.",font=f(29,serif=True),fill=(237,243,249,255))
d.text((x,452),"Просто о сложном.",font=f(29,serif=True),fill=(237,243,249,255))
d.text((36,559),"Верхняя Пышма  ·  Екатеринбург  ·  Среднеуральск",font=f(22),fill=(239,243,250,255))
im.convert("RGB").save("og-preview.jpg",quality=93,subsampling=0,optimize=True)
print("Generated og-preview.jpg and qr-website.png")
