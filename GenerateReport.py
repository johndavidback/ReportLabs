from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, cm, letter, inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.graphics.shapes import *
from io import BytesIO

buffer = BytesIO()
file = open('Employee_Survey.pdf', 'w+')

width, height = letter
styles = getSampleStyleSheet()
styleN = styles['BodyText']
styleN.alignment = TA_LEFT

headerStyle = styles['Normal']
headerStyle.alignment = TA_CENTER
headerStyle.fontSize = 7
headerStyle.fontName = 'Helvetica-Bold'

def coord(x, y, unit=1):
    x, y = x * unit, height -  y * unit
    return x, y

def draw_grid(canvas):
    GRID_COLOR = (0.5, 0.5, 1)
    INTERVAL = 5 * mm

    numv = int((width - ((4 + 4) * mm)) / INTERVAL)
    numh = int((height - (16 + 3) * mm) / INTERVAL)
    voff = (width - numv * INTERVAL) / 2.0
    hoff = 16 * mm

    # Draw
    c = canvas
    c.setLineWidth(0.15)
    c.setStrokeColorRGB(*GRID_COLOR)
    for xi in xrange(numv + 1):
        c.line(xi * INTERVAL + voff, hoff,
               xi * INTERVAL + voff, hoff + numh * INTERVAL)
    for yi in xrange(numh + 1):
        c.line(voff, hoff + yi * INTERVAL,
               voff + numv * INTERVAL, hoff + yi * INTERVAL)
    #c.circle(width / 2, 5 * mm, 0.7, fill=1)

#Create the Header
def build_percent_responding_rectangles(percentFavorable,percentNeutral,percentUnfavorable,header=False):

    #Header Rectangles

    percentFavorableFloat = float(percentFavorable)/100
    percentNeutralFloat = float(percentNeutral)/100
    percentUnfavorableFloat = float(percentUnfavorable)/100
    if header:
        d = Drawing(0*mm, 10*mm)

    else:
        d = Drawing(0*mm, 0*mm)

    totalRectangleLength = 60
    rectangleHeight = 4
    rectangleYposition = 0
    rectangleTextYposition = 1
    rectangleTextHeight = 2.5


    #Favorable rect
    favorableXposition = 0
    favorableRectWidth = percentFavorableFloat*totalRectangleLength
    if header:
        favorableRectTextXPosition = favorableXposition + 1
        favorableRectText = '% Favorable'
    else:
        favorableRectTextXPosition = (favorableXposition +favorableRectWidth)/2
        favorableRectText = str(percentFavorable)

    d.add(Rect(favorableXposition*mm, rectangleYposition*mm, favorableRectWidth*mm, rectangleHeight*mm, fillColor=colors.green))
    d.add(String(favorableRectTextXPosition*mm, rectangleTextYposition*mm, favorableRectText, fontSize=rectangleTextHeight*mm,fontName='Helvetica'))

    #Neutral Rect
    neutralXposition = favorableRectWidth
    neutralRectWidth = percentNeutralFloat*totalRectangleLength
    if header:
        neutralRectTextXPosition = neutralXposition + 1
        neutralRectText = '% Neutral'
    else:
        neutralRectTextXPosition = (neutralXposition + neutralRectWidth + favorableRectTextXPosition)/2
        neutralRectText = str(percentNeutral)

    d.add(Rect(neutralXposition*mm, rectangleYposition*mm, neutralRectWidth*mm, rectangleHeight*mm, fillColor=colors.yellow))
    d.add(String(neutralRectTextXPosition*mm, rectangleTextYposition*mm, neutralRectText, fontSize=rectangleTextHeight*mm,fontName='Helvetica'))

    #Unfavorable Rect
    unfavorableXposition = neutralRectWidth + favorableRectWidth
    unfavorableRectWidth = (percentUnfavorableFloat*totalRectangleLength)
    if header:
        unfavorableRectTextXPosition = unfavorableXposition + 1
        unfavorableRectText = '% Unfavorable'
    else:
        unfavorableRectTextXPosition = (unfavorableXposition + unfavorableRectWidth + favorableRectTextXPosition + neutralRectTextXPosition)/2
        unfavorableRectText = str(percentUnfavorable)

    d.add(Rect(unfavorableXposition*mm, rectangleYposition*mm, unfavorableRectWidth*mm, rectangleHeight*mm, fillColor=colors.red))
    d.add(String(unfavorableRectTextXPosition*mm,rectangleTextYposition*mm, unfavorableRectText, fontSize=rectangleTextHeight*mm,fontName='Helvetica'))

    if header:
        #Percent Responding Heading text
        percentResponseTextXposition = 15
        percentResponseTextYposition = 5
        percentResponseText = 'Percent Responding'
        d.add(String(percentResponseTextXposition*mm,percentResponseTextYposition*mm, percentResponseText, fontSize=7, fontName='Helvetica-Bold'))
    return d


percentRespondingHeader = build_percent_responding_rectangles(33, 33, 33, header=True)
chart = build_percent_responding_rectangles(33, 33, 33, header=False)
perfMgmtHeader = Paragraph('''<b>Perfomance Managment</b>''', headerStyle)
totalNheader = Paragraph('''<b>Total N</b>''', headerStyle)
percentResp = Paragraph('''<b>Percent Responding</b>''', headerStyle)
percentFavHeader = Paragraph('''<b>% Fav</b>''', headerStyle)
percentDistHeader = Paragraph('''<b>% Distribution</b>''', headerStyle)
meanHeader = Paragraph('''<b>Mean</b>''', headerStyle)
data= [[perfMgmtHeader, totalNheader,percentRespondingHeader, percentFavHeader, percentDistHeader,meanHeader],
       ['10', '11', chart, '13', '14', '15'],
       ['20', '21', '22', '23', '24', '25'],
       ['30', '31', '32', '33', '34', '35'],
       ['40', '41', '42', '43', '44', '45'],
]

#Style the table
t = Table(data,style=[
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ('FONTSIZE',(0, 0), (-1, -1), 7),
    #('ALIGN', (0,0), (-1,1), 'LEFT'),
    #('BACKGROUND',(0,2),(-1,-1),colors.green)
    #('LINEABOVE',(0,1),(-1,1),1,colors.rgb2cmyk(1,1,1)),
    #('SPAN',(0,1),(-1,1)),
])

# Fixed column widths
t._argW[0] = 50.8*mm #Perf Mgmt
t._argW[1] = 12.7*mm #Total N
t._argW[2] = 63.5*mm # % Resp
t._argW[3] = 12.7*mm # % Fav
t._argW[4] = 38.1*mm # % Dist
t._argW[5] = 10.922*mm # Mean

c = canvas.Canvas(buffer, pagesize=letter)
t.wrapOn(c, width, height)
t.drawOn(c, *coord(5, 60, mm))
#drawGrid(c)
c.save()

#Write the buffer to disk and close the file
pdf = buffer.getvalue()
file.write(pdf)
buffer.close()
file.close()
