from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.colors import yellow, red, black, green
from reportlab.lib.pagesizes import letter, inch
from io import BytesIO

def variousshapes(canvas):
    from reportlab.lib.units import inch
    inch = int(inch)
    canvas.setStrokeGray(0.5)
    canvas.grid(range(0,int(11*inch/2),int(inch/2)), range(0,int(7*inch/2),int(inch/2)))

    rectangeHieght = .5
    # % Favorable
    favorableXposition = inch
    favorableYposition = inch
    favorableRectWidth = 1*inch

    # Favorable Rect
    canvas.setStrokeColor(green)
    canvas.setFillColor(green)
    canvas.rect(favorableXposition,favorableYposition,favorableRectWidth,rectangeHieght*favorableYposition, fill=1)

    # % Favorable Text
    canvas.setFillColor(black)
    canvas.drawString(favorableXposition+(favorableXposition/2.5),favorableYposition+(favorableYposition/5), "11")

    # % Neutral
    neutralXposition = 2*inch
    neutralYposition = 1*inch
    neutralRectWidth = 1*inch

    # Neutral Rect
    canvas.setStrokeColor(yellow)
    canvas.setFillColor(yellow)
    canvas.rect(neutralXposition,neutralYposition,neutralRectWidth,rectangeHieght*inch, fill=1)

    # % Neutral Text
    canvas.setFillColor(black)
    canvas.drawString(neutralXposition+(neutralXposition/2.5),neutralYposition+(neutralYposition/5), "22")

    # % Unfavorable
    unfavorableXposition = 3*inch
    unfavorableYposition = 1*inch
    unfavorableRectWidth = 1*inch

    # Unfavorable Rect
    canvas.setStrokeColor(red)
    canvas.setFillColor(red)
    canvas.rect(unfavorableXposition,unfavorableYposition,unfavorableRectWidth,rectangeHieght*inch, fill=1)

    # Unfavorable Text
    canvas.setFillColor(black)
    canvas.drawString(unfavorableXposition+(unfavorableXposition/2.5),unfavorableYposition+(unfavorableYposition/5), "33")


buffer = BytesIO()
file = open('rects.pdf', 'w+')

width, height = letter
c = canvas.Canvas(buffer, pagesize=letter)
variousshapes(c)
c.save()

#Write the buffer to disk and close the file
pdf = buffer.getvalue()
file.write(pdf)
buffer.close()

file.close()
