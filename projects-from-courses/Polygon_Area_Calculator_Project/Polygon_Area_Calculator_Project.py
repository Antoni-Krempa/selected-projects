class Rectangle:
    def __init__(self,width,height):
        self.width = width
        self.height = height


    def set_width(self,new_width):
        self.width = new_width

    def set_height(self,new_height):
        self.height = new_height


    def get_area(self):
        area = self.width * self.height
        return area

    def get_perimeter(self):
        return 2*self.width + 2*self.height
        
    def get_diagonal(self):
        return (self.width**2 + self.height**2)**0.5
    
    def get_picture(self):
        if (self.width >50) or (self.height > 50):
            return 'Too big for picture.'

        picture = ''
        
        for i in range(self.height):
            for j in range(self.width):
                picture += '*'
            picture += '\n'

        return picture
    def __str__(self):
        return f"Rectangle(width={self.width}, height={self.height})"

    def get_amount_inside(self,shape):
    
        height_times = self.height//shape.height
        width_times = self.width//shape.width

        return height_times*width_times

        
        
        

        

    



class Square(Rectangle):
    def __init__(self,side):
        self.width = side
        self.height = side


    def set_side(self,side):
        self.width = side
        self.height = side

    def set_width(self,new_width):
        self.width = new_width
        self.height = new_width

    def set_height(self,new_height):
        self.height = new_height
        self.width = new_height


    

    def __str__(self):
        return f"Square(side={self.width})"


    

rect = Rectangle(10, 5)
print(rect.get_area())
rect.set_height(3)
print(rect.get_perimeter())
print(rect)
print(rect.get_picture())

sq = Square(9)
print(sq.get_area())
sq.set_side(4)
print(sq.get_diagonal())
print(sq)
print(sq.get_picture())

rect.set_height(8)
rect.set_width(16)
print(rect.get_amount_inside(sq))

print(Rectangle(4,8).get_amount_inside(Rectangle(3, 6)))