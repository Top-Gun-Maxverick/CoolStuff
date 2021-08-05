import turtle

window = turtle.Screen()
window.setup(width=800, height=600, startx=10, starty=0.5)
blahaj = turtle.Turtle() 
blahaj.shape("turtle")
scale = 5 
blahaj.penup()
blahaj.setpos(-390, 0)
blahaj.pendown()

current = 0  
seen = set()
for step_size in range(1, 100):

    backwards = current - step_size
    if backwards > 0 and backwards not in seen:
        blahaj.setheading(90)
        blahaj.circle(scale * step_size/2, 180)
        current = backwards
        seen.add(current)

    else:
        blahaj.setheading(270) 
        blahaj.circle(scale * step_size/2, 180)
        current += step_size
        seen.add(current)

turtle.done()
