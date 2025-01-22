"""
PROGRAM TITLE: Math Test
AUTHOR: Stephen Lukner
DATE COMPLETED (last edit): 3/24/23
PROGRAM PURPOSE: Program tests the math skills of a user with 5 questions, one from each of the 
                 following categories: "Addition and Subtraction," "Multiplicaiton," "Division,"
                 "Geometry," and "Quadratic Roots"
PROGRAM SUMMARY: Program randomly generates a simple math question from each of the above topics and 
                 uses the customtkinter GUI module to display each question and allow a user to input
                 their answer, subsequently telling the user if their answer was correct or not. After
                 completing all questions, the GUI window displays the number of questions the user
                 answered correctly.
"""
import random
import operator
import copy
import math
import tkinter as tk
import customtkinter as ctk

# RANDOMIZED MATH QUESTION GENERATION SECTION (MAIN CODE SECTION 1)

PI = 3.14

# operators used for answer calculation of add/sub and mul questions and during gen of div questions
OPS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
}

# Question class objects used in question generation functions (all in MAIN CODE SECTION 1) to return all 
#   attributes of a question used in the display and testing of question (string, answer, and category)
class Question:

    def __init__(self, question_str, answer, question_category):
        self.question_str = question_str
        self.answer = answer
        self.cat = question_category


# function rounds with conventional rounding rules rather than Python rounding rules. (Python rounds .5 to
# nearest even number, so 2.5 rounds to 2. This is uncommon for the way most people learn math.)
def correct_round(num):
    dec = num - math.floor(num)
    if dec < 0.5: 
        return math.floor(num)
    else:
        return math.ceil(num)




# function generates random 2 term addition or subtraction problem with integers only up to 2 digits
#   per term.
def get_add_sub_question():
    n1 = random.randint(-99, 99)
    n1_str = str(n1)
    op = "+"
    n2 = random.randint(-99, 99)
    n2_str = str(n2)


    if random.randint(0, 1):       # 50% chance that question is subtraction
        op = "-"
    if n2 < 0:
        n2_str = f"({n2_str})"
    
    question_str = f"{n1_str}{op}{n2_str}"
    answer = OPS[op](n1, n2)

    add_sub_question = Question(question_str, answer, "Addition and Subtraction")
    return add_sub_question

# function generates random 2 integer multiplication problem (up to 12 * 12)
def get_mul_question():
    multiplicand = random.randint(-12, 12)
    multiplicand_str = str(multiplicand)
    multiplier = random.randint(-12, 12)
    multiplier_str = str(multiplier)
    if multiplier < 0:
        multiplier_str = f"({multiplier_str})"

    
    question_str = f"{multiplicand_str}*{multiplier_str}"
    product = multiplicand * multiplier

    mul_question = Question(question_str, product, "Multiplication")

    return mul_question

# function generates random 2 integer division problem (3 or 4 digit dividend and 2 digit divisor)
def get_div_question():
    dividend = 0
    divisor = 1
    quotient = 1

    # while loop runs until dividend is 3 or 4 digits
    while abs(dividend) < 100 or abs(dividend) >= 10000:
        quotient = random.randint(-99, 99)  # gens quotient first so that quotient is ensured to be int
        divisor = random.randint(-99, 99)
        dividend = quotient * divisor       # dividend found from quotient and divisor so all are ints
    dividend_str = str(dividend)
    divisor_str = str(divisor)
    if divisor < 0:
        divisor_str = f"({divisor_str})"
    
    question_str = f"{dividend_str}/{divisor_str}"

    div_question = Question(question_str, quotient, "Division")
    return div_question


# Shape class objects used in generation of geometry question in get_geometry_question() function.
# Shape objects store the attributes of different 2D and 3D shapes so that the correct string and formula
#   is used for specific shape type with varying random values for length, width, and height.
class Shape:
    len = 0                         # length of shape
    wid = 0                         # width of shape
    hei = 0                         # height of shape

    # end of geometry question sentence with different names for lengths of different parts of various 
    # shapes (e.g. length is called radius when circle, width called height when triangle, etc.)
    prompt_end = "none"             
    base_shape = Question(1, 1, 1)  # base shape object for prisms and pyramids
    prism_pyramid = "neither"       # changes to string of either "prism" or "pyramid" if shapes is either

    def __init__(self, name, is_two_dimensional):
        self.name = name
        self.is_two_dimensional = is_two_dimensional



# function finds the area of 2D Shape object (square, rectangle, triangle, or circle)
# used in both 2D geometry questions and 3D geometry questions with prisms and pyramids
def get_2D_area(shape):
    if shape.name == "square" or shape.name == "rectangle":
        return shape.len * shape.wid
    elif shape.name == "triangle":
        return shape.len * shape.wid * (1/2)
    else:
        return PI * (shape.len ** 2)
    
# function finds the perimeter of a 2d Shape object (square, rectangle, or circle)
# used in both 2D geometry questions and 3D geometry questions with prisms
def get_2D_perimeter(shape):
    if shape.name == "square" or shape.name == "rectangle":
        return 2 * (shape.len + shape.wid)
    elif shape.name == "circle":
        return PI * shape.len * 2


# function finds the answer to geometry question using passed Shape object attributes
def get_geometry_answer(shape, asking):
    if shape.is_two_dimensional:
        if asking == "area":
            return get_2D_area(shape)                       # area of 2D shape
        elif asking == "perimeter":
            return get_2D_perimeter(shape)                  # perimeter of 2D shape
    else:
        if asking == "volume":
            if shape.prism_pyramid != "neither":
                base_area = get_2D_area(shape.base_shape)
                if shape.prism_pyramid == "prism":
                    return base_area * shape.hei            # volume of prism
                else:
                    return base_area * shape.hei * (1/3)    # volume of pyramid
            else:
                return (4/3) * PI * (shape.len ** 3)        # volume of sphere
        elif asking == "surface area":
            if shape.prism_pyramid == "prism":
                base_area = get_2D_area(shape.base_shape)
                base_perimeter = get_2D_perimeter(shape.base_shape)
                return 2 * base_area + base_perimeter * shape.hei   # surface area of prism 
            else:
                return 4 * PI * shape.len ** 2                      # surface area of sphere
    raise Exception("issue in get_geometry_answer function")




# function generates a random geometry word problem asking for the area or perimeter of a 2D shape or
#   the volume or surface area of a 3D shape
def get_geometry_question():
    # list of Shape objects tested in geometry questions
    shapes = [
        # 2D:
        Shape("square", True),
        Shape("rectangle", True),
        Shape("triangle", True),
        Shape("circle", True),
        # 3D:
        Shape("prism", False),
        Shape("pyramid", False),
        Shape("sphere", False)
    ]

    asking = "area"   # asking holds what geometry question will be "asking for" (e.g. area, volume, etc.)
    rand_int = random.randint(0, 1)     # random number will choose between area, perim, vol, or surf area
    shape = copy.deepcopy(shapes[random.randint(0, len(shapes) - 1)])   # random shape from shapes list
    shape.len = random.randint(1, 10)   # shape length
    shape.wid = random.randint(1, 10)   # shape width (even if not used)
    while shape.wid == shape.len:           # while loop prevents accidental squares
        shape.wid = random.randint(1, 10)
    shape.hei = random.randint(1, 10)   # shape height (even if not used)
    shape.pi_question = ""              # if question involves pi, user told to use 3.14 for pi


    # following if statements organize question_str primarily based on random variables found above 
    if shape.is_two_dimensional:
        if rand_int == 1 and shape.name != "triangle":
            asking = "perimeter"
        
        if shape.name == "square" or shape.name == "circle":
            if shape.name == "square":
                shape.wid = shape.len
                shape.prompt_end = f"side length of {shape.len}"
            else:
                shape.prompt_end = f"radius of {shape.len}"
                shape.pi_question = " Use 3.14 for π."
        else:
            if shape.name == "triangle":
                shape.prompt_end = f"base length of {shape.len} and a height of {shape.wid}"
            else:
                shape.prompt_end = f"length of {shape.len} and a width of {shape.wid}"
    else:   # else runs if shape is 3D (prism, pyramid, or sphere)
        asking = "volume"
        if rand_int == 1:
            asking = "surface area"

        if shape.name == "prism" or shape.name == "pyramid":
            if shape.name == "prism":
                shape.prism_pyramid = "prism"
            else:
                shape.prism_pyramid = "pyramid"
                asking = "volume"
            
            shape.base_shape = copy.deepcopy(shapes[random.randint(0, 3)])
            shape.base_shape.len = shape.len
            shape.base_shape.wid = shape.wid


            if shape.base_shape.name != "circle":
                if shape.base_shape.name == "triangle":
                    asking = "volume"
                    shape.name = "triangular " + shape.name
                elif shape.base_shape.name == "rectangle":
                    shape.name = "rectangular " + shape.name

                if shape.base_shape.name == "square":
                    shape.wid = shape.len
                    shape.base_shape.wid = shape.len
                    shape.prompt_end = f"side length of {shape.len} and a height of {shape.hei}"
                    if shape.name == "pyramid":
                        shape.name = "square " + shape.name
                    else:
                        shape.name = "cube"
                        shape.hei = shape.len
                        shape.base_shape.hei = shape.len
                        shape.prompt_end = f"side length of {shape.len}"
                else:
                    shape.prompt_end = (
                        f"length of {shape.len}, "
                        f"width of {shape.wid}, "
                        f"and a height of {shape.hei}"
                    )
            else:
                shape.pi_question = " Use 3.14 for π."
                shape.prompt_end = f"radius of {shape.len} and a height of {shape.hei}"
                if shape.name == "pyramid":
                    shape.name = "cone"
                else:
                    shape.name = "cylinder"
        else:
            shape.prompt_end = f"radius of {shape.len}"
            shape.pi_question = " Use 3.14 for π."
    
    prompt = (
        f"What is the {asking} of a {shape.name} with a {shape.prompt_end}?"
        f"{shape.pi_question} (Round to the nearest whole number if needed)"
    )
    answer = correct_round(get_geometry_answer(shape, asking))
    question = Question(prompt, answer, "Geometry")

    return question




# function finds factors (excluding 1) of an inputted integer number x.
# function returns all factors of a number in an integer list (smallest to largest).
def factor_finder(x):
    x = str(x)
    factor_list = []
    if x[0] == "-":
        x = x[1:len(x)]
    x = int(x)
    for i in range(2, x + 1):
        if x % i == 0:
            factor_list.append(i)
    return factor_list


# function simplifies a fraction by factoring out gcf common factors of two 
# passed numbers: numerator and denominator
def simplify_frac(numerator, denominator):

    numerator_factors = factor_finder(numerator)
    denominator_factors = factor_finder(denominator)

    # n1_factors is reversed to find greatest common factor (gcf) instead of least common factor that
    #   might leave fraction not fully simplified
    for i in reversed(numerator_factors):
        if i != 1:
            for j in reversed(denominator_factors):
                if i == j:
                    numerator = correct_round(numerator / i)
                    denominator = correct_round(denominator / i)
                    return [numerator, denominator]             # returns to stop loop at gcf 
    return [numerator, denominator]                             # returns same frac if no common factors



# Function generates a random quadratic expression equal to 0 with integer roots.
# All quadratic equation questions can be solved through one of the four following methods:
#   Difference of two squares
#   Perfect square trinomial
#   Factor without coefficient in first term
#   Factor by grouping (Find roots with coefficient in first term)
def get_quad_question():
    question_str = "Error"
    answer = 1
    denominator = "no d"
    term1 = "x^2"
    term2 = ""
    term3 = ""
    gcf = random.randint(0, 1)  
    if gcf == 0:    # quadratic has 50% chance of having a gcf to factor out before factoring to solve
        gcf = random.randint(1, 10)
    root1 = 0
    while root1 == 0:
        root1 = random.randint(-10, 10)
    root2 = 0
    while root2 == 0:
        root2 = random.randint(-10, 10)


    # diff of squares, perf square trinomial, and factor by grouping quads all have 1 in 5 chance
    #   of being factor type, but factoring without coefficient in front of x^2 has 2 in 5 chance
    # Purpose of having 2 in 5 chance is because that type of quadratic is much, much more common
    #   in most math problems involving quadratics and quadratic roots.
    factor_type = random.randint(1, 5)
    
    # difference of two squares
    if factor_type == 1:
        root2 = -1 * root1
        if gcf != 1:
            term1 = f"{gcf}x^2"
            term2 = str(correct_round(gcf * (root1 ** 2)))
        else:
            term2 = str(correct_round(root1 ** 2))
        question_str = f"{term1} - {term2}"
        answer = [str(root1), str(root2)]

    # perfect square trinomial
    elif factor_type == 2:
        root1 = abs(root1)
        root2 = 100
        is_neg = random.randint(0, 1)
        if gcf != 1:
            term1 = f"{gcf}x^2"
            term2 = f"{gcf * (2 * root1)}x"
            term3 = f"{gcf * correct_round(root1 ** 2)}"
        else:
            term2 = f"{(2 * root1)}x"
            term3 = str(correct_round(root1 ** 2))
        if is_neg:
            question_str = f"{term1} + {term2} + {term3}"
            answer = [str(-1 * root1)]
        else:
            question_str = f"{term1} - {term2} + {term3}"
            answer = [str(root1)]

    # factor without coefficient in first term
    elif factor_type == 3 or factor_type == 4:
        while abs(root1) == abs(root2):
            root2 = random.randint(-10, 10)
            while root2 == 0:
                root2 = random.randint(-10, 10)
        if gcf != 1:
            term1 = f"{gcf}x^2"
            term2 = f"{gcf * ((-1 * root1) + (-1 * root2))}x"
            term3 = str(gcf * ((-1 * root1) * (-1 * root2)))
        else:
            term2 = f"{(-1 * root1) + (-1 * root2)}x"
            term3 = str((-1 * root1) * (-1 * root2))
        
        term2 = quad_term_formatter(term2)
        term3 = quad_term_formatter(term3)

        question_str = f"{term1}{term2}{term3}"
        answer = [str(root1), str(root2)]
        
    # factor by grouping
    elif factor_type == 5:
        denominator = root1
        denominator = random.randint(1, 10)

        while float(int(root1/denominator)) == root1/denominator:
            denominator= random.randint(1, 10)


        simplified_frac = simplify_frac(root1, denominator)
        root1 = simplified_frac[0]
        denominator = simplified_frac[1]
        if gcf != 1:
            term1 = f"{gcf * denominator}x^2"
            term2 = f"{gcf * ((-1 * root1) + (-1 * denominator * root2))}x"
            term3 = str(gcf * ((-1 * root1) * (-1 * root2)))
        else:
            term1 = f"{denominator}x^2"
            term2 = f"{(-1 * root1) + (-1 * denominator * root2)}x"
            term3 = f"{(-1 * root1) * (-1 * root2)}"
        
        term2 = quad_term_formatter(term2)
        term3 = quad_term_formatter(term3)


        question_str = f"{term1}{term2}{term3}"
        answer = [f"({root1}/{denominator})", str(root2)]
    else:
        raise Exception("Error in Math_test.py get_quad_question() function. factor_type is not 1-5")


    # set quadratic expression equal to 0 to allow user to solve for x as an equation
    question_str = question_str + " = 0"
    question = Question(question_str, answer, "Quadratic Roots")
    return question

# formats the 2nd and 3rd term strings of factor types 3-5 (e.g. ensures -23x does not format as "+ -23x")
def quad_term_formatter(term_str):
    if term_str[0 : 1] == "-":
        return f" - {term_str[1 : len(term_str)]}"
    else:
        return f" + {term_str}"

# calls all five question generation functions and returns all 5 Question objects in the form of a list
def get_question_list():
    question_list = [
        get_add_sub_question(),
        get_mul_question(),
        get_div_question(),
        get_geometry_question(),
        get_quad_question()
    ]
    return question_list






# FRONT END AND USER TESTING SECTION (MAIN CODE SECTION 2)





# App class creates customtkinter window object
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("light")
        self.title("Math Test")
        self.geometry("400x500")
        self.resizable(False, False)


# MathTest class creates principal CTkFrame within App object in which all customtkinter widgets for
#   the Math Test are created, stored, and displayed.
class MathTest(ctk.CTkFrame):

    question_list = get_question_list()     # list of 5 Question objects, one from each question type
    correct_answers = 0                     # counter of user correct answers in one MathTest instance

    def __init__(self, master_root):
        super().__init__(master_root)
        self.master_root = master_root          # sets App object as Frame widget's master

        # self.question is Question object from question_list that is currently displayed to user
        self.question = self.question_list[0]

    # method displays the initial introduction screen to the MathTest, explaining how 5 subjects are 
    #   tested (one from each of the question generation methods)
    def disp_intro_screen(self):
        self.intro_frame = ctk.CTkFrame(master=self.master_root,
                                        fg_color="transparent")

        # lbl_intro appears as title when first running program
        intro_text = tk.StringVar(value = "Math Test")
        self.lbl_intro = ctk.CTkLabel(master=self.intro_frame,
                                        textvariable=intro_text,
                                        font=("Bauhaus 93", 50),
                                        pady=10)
        self.lbl_intro.pack()

        # lbl_sub_intro prompts user with purpose of test and what will follow
        sub_intro_str = (
            "Test your math skills!\n"
            "Solve one problem from each of\n"
            "the following five categories:\n"
        )
        sub_intro_tk_str = tk.StringVar(value = sub_intro_str)
        self.lbl_sub_intro = ctk.CTkLabel(master=self.intro_frame,
                                        textvariable=sub_intro_tk_str,
                                        font=("Cascadia Code Bold", 20))
        self.lbl_sub_intro.pack()
        
        # txt_cats shows all five question categories tested in Math Test program
        self.txt_cats = ctk.CTkTextbox(master=self.intro_frame, 
                                   font=("Cascadia Code Bold", 20),
                                   activate_scrollbars=False,
                                   fg_color="transparent",
                                   width=375,
                                   height=175)
        cats = (
            "• Addition and Subtraction\n"
            "• Multiplication\n"
            "• Division\n"
            "• Geometry\n"
            "• Quadratic Roots\n"
        )
        self.txt_cats.insert(0.0, cats)
        self.txt_cats.configure(state="disabled")
        self.txt_cats.pack()

        # btn_start is start button to begin the test and give first question
        self.btn_start = ctk.CTkButton(master=self.intro_frame,
                                       width=200,
                                       height=50,
                                       border_width=4,
                                       border_spacing=10,
                                       text="Start",
                                       font=("Cascadia Code Bold", 30),
                                       command=start_test)
        self.btn_start.pack(pady=20)

        self.intro_frame.pack()



        self.gen_test_widgets()     # generating test widgets needed for displaying Questions

    
    # generates the widgets used to display each question to user (no input) and next question button
    def gen_test_widgets(self):
        self.question_number = self.question_list.index(self.question) + 1

        # upper_frame is all widgets to display Question problem. 
        # Does not take input from user or change within single question based on user input.
        self.upper_frame = ctk.CTkFrame(master=self.master_root,
                                        fg_color="transparent")

        # self.lbl_header attrs display the question number and category of question at top of window
        self.lbl_header_text = tk.StringVar(value = f"#{self.question_number}")
        self.lbl_header = ctk.CTkLabel(master=self.upper_frame,
                                  textvariable=self.lbl_header_text,
                                  font=("Bauhaus 93", 30),
                                  pady=15)
        self.lbl_header.pack()
        

        # self.lbl_prompt attrs display prompt proceeding the math expression in non-geometry Questions
        self.prompt_text = "Simplify the following expression:\n"
        self.lbl_prompt_text = tk.StringVar(value = self.prompt_text)
        self.lbl_prompt = ctk.CTkLabel(master=self.upper_frame,
                                  textvariable=self.lbl_prompt_text,
                                  font=("Cascadia Code Bold", 19))
        self.lbl_prompt.pack()
        
        # self.lbl_question display the current Question object's question_str attribute
        self.lbl_question = ctk.CTkLabel(master=self.upper_frame,
                                    textvariable=self.lbl_prompt_text, # placeholder textvariable
                                    font=("Cascadia Code Bold", 40))
        self.lbl_question.pack()
        
        # self.txt_long_prompt attrs display geometry word problem Questions and the answer rules for quad
        self.long_prompt_text = "long_prompt_text"  #placeholder text
        self.txt_long_prompt = ctk.CTkTextbox(master=self.upper_frame,
                                              fg_color="transparent",
                                              width=370,
                                              height = 140,
                                              activate_scrollbars=False,
                                              font=("Cascadia Code Bold", 18),
                                              wrap = "word")
        
        # btn_frame1 and btn_frame2 used to pack locked and unlocked btn_next widgets in bot-right corner
        self.btn_frame1 = ctk.CTkFrame(master=self.master_root,
                                       fg_color="transparent")
        self.btn_frame2 = ctk.CTkFrame(master=self.btn_frame1,
                                       fg_color="transparent")
        
        # unclickable next button. (no input) Displayed when user has not yet answered the given question
        self.btn_next_locked = ctk.CTkButton(master=self.btn_frame2,
                                       fg_color="light gray",
                                       text_color="dark gray",
                                       border_color="dark gray",
                                       width=150,
                                       height=30,
                                       border_width=3,
                                       border_spacing=5,
                                       text="Next",
                                       state="disabled",
                                       font=("Cascadia Code Bold", 20))
        
        # clickable next button. (takes mouse click input) Displayed when user has answered given question
        self.btn_next = ctk.CTkButton(master=self.btn_frame2,
                                      hover_color="#3f9e2e",
                                      text_color="black",
                                      border_color="black",
                                      fg_color="#52d43b",
                                       width=150,
                                       height=30,
                                       border_width=3,
                                       border_spacing=5,
                                       text="Next",
                                       font=("Cascadia Code Bold", 20),
                                       command=next_question)
        

        
    # method generates all widgets in lower area of each question screen
    # Answer area widgets take input from user and can/will change appearance based on user input
    def gen_answer_area(self):
        self.answer_area = ctk.CTkFrame(master=self.master_root,
                                        fg_color="transparent")
        
        # lbl_error attrs display error message to user if an incompatible or blank answer is given
        self.error_text = tk.StringVar(value=" ")
        self.lbl_error = ctk.CTkLabel(master=self.answer_area,
                                 textvariable=self.error_text,
                                 font=("Cascadia Code Bold", 17),
                                 text_color="red")
        self.lbl_error.pack(pady=5)

        # ent_answer takes input (user's answer) in the from of a string
        self.ent_answer = ctk.CTkEntry(master=self.answer_area,
                                  width=200,
                                  height=50,
                                  placeholder_text="Answer",
                                  border_color="black",
                                  font=("Cascadia Code Bold", 20))
        self.ent_answer.pack()
        
        # btn_submit takes mouse click input to submit the string answer given in ent_answer widget
        self.btn_submit = ctk.CTkButton(master=self.answer_area,
                                       width=100,
                                       height=25,
                                       border_width=2,
                                       border_spacing=5,
                                       text="Submit",
                                       font=("Cascadia Code Bold", 15),
                                       command=submit_answer)
        
        self.btn_submit.pack(pady=10)
        
        # lbl_give_answer attrs disp the correct answer to user if user gave incorrect answer to Question
        self.give_answer_text = ""
        self.lbl_give_answer = ctk.CTkLabel(master=self.answer_area,
                                            width=150,
                                            textvariable=tk.StringVar(value=self.give_answer_text),
                                            fg_color="transparent",
                                            text_color="black",
                                            font=("Cascadia Code Bold", 20))
        self.lbl_give_answer.pack()

        
        self.btn_next_locked.pack(padx=20,
                                  pady=20)
        
        # packing frames for next buttons (btn_next_locked and btn_next) in bottom right corner
        self.btn_frame2.pack(side=tk.RIGHT)
        self.btn_frame1.pack(fill=tk.X,
                             side=tk.BOTTOM)
        
        self.answer_area.pack(side=tk.BOTTOM)

        # runs question_sequencer to go to configure and display 1st question or next question
        self.question_sequencer()



    def question_sequencer(self):
        self.close_next_btn()       # locks next_btn to be unclickable until user answers question
        
        # resets ent_answer to take input again and have gray background (from previous green or red)
        self.ent_answer.configure(fg_color="#F9F9FA",
                                  placeholder_text="Answer",
                                  state="normal")
        # clears last answer in ent_answer
        self.ent_answer.delete(first_index=0, last_index=len(self.ent_answer.get()))

        # clears lbl_error from previous question
        self.error_text = tk.StringVar(value = " ")
        self.lbl_error.configure(textvariable=self.error_text)
        
        
        # sets MathTest current question object (self.question) to next Question object in question_list
        self.question = self.question_list[self.question_number - 1] 
        print(f"Answer: {self.question.answer}")                                                          # REMOVE IN FINAL SUBMISSION

        # changes question header to question number with with self.question's category
        self.lbl_header_text = tk.StringVar(value = f"#{self.question_number} {self.question.cat}")
        self.lbl_header.configure(textvariable=self.lbl_header_text)
        
        
        # if true, lbl_question (the actual expression) is displayed for expression questions
        if self.question_number <= 3:
            self.lbl_question_text = tk.StringVar(value = self.question.question_str)
            self.lbl_question.configure(textvariable=self.lbl_question_text)
        # else, geometry and quadratic questions remove lbl_question and display differently
        else:
            # if true, displays geometry question as uneditable text widget
            if self.question_number == 4:
                self.lbl_question.pack_forget()
                self.lbl_prompt.pack_forget()
                self.txt_long_prompt.insert(0.0, text = self.question.question_str)
                self.txt_long_prompt.configure(state = "disabled")
            # else, displays quadratic question with certain conditions for user's answer
            else:
                self.txt_long_prompt.pack_forget()
                self.txt_long_prompt.configure(state = "normal",
                                               height = 100,
                                               font = ("Cascadia Code Bold", 16))
                self.txt_long_prompt.delete(0.0, 12.0)
                quad_answer_conditions = (
                    "If two x values are found, separate them with \"and\" (ex. \"-2 and 17\")."
                    "If a fraction x value is found, type it in parentheses (ex. \"(11/3)\")."
                )
                self.txt_long_prompt.insert(0.0, quad_answer_conditions)

                
                quad_prompt = "Solve for all value(s) of x:\n"
                self.lbl_prompt.configure(textvariable = tk.StringVar(value = quad_prompt))
                self.lbl_prompt.pack()

                lbl_question_text = tk.StringVar(value = self.question.question_str)
                self.lbl_question.configure(textvariable = lbl_question_text,
                                            font = ("Cascadia Code Bold", 28))
                self.lbl_question.pack()
            self.txt_long_prompt.pack()

        # increases question number by 1 to sequence to next question upon next question_sequencer() call
        self.question_number += 1

    # method determines if user's inputted answer equals the Question object's answer
    def input_equals_answer(self):

        self.open_next_btn()        #opens next button to allow user to go to next question or finish

        # if user's answer is correct
        if self.user_answer == self.question.answer:
            self.correct_answers += 1
            self.error_text = tk.StringVar(value = "Correct!")
            self.lbl_error.configure(textvariable=self.error_text,
                                    text_color="green")
            
            # turns answer entry box red and locks entry box from changing answer
            self.ent_answer.configure(fg_color="#86ff80",
                                    state="disabled")
        # else runs if user's answer is incorrect
        else:
            # if quadratic question, 
            if self.question_number == 6:
                correct_answer = "Correct answer: "
                if len(self.question_list[self.question_number - 2].answer) == 2:
                    correct_answer = (
                        correct_answer +
                        self.question_list[self.question_number - 2].answer[0] +
                        " and " +
                        self.question_list[self.question_number - 2].answer[1]
                    )
                else:
                    self.give_answer = correct_answer + self.question_list[self.question_number - 2].answer[0]
            else:
                self.give_answer = f"Correct answer: {self.question_list[self.question_number - 2].answer}"
            
            # provides user with correct answer upon submitting incorrect answer
            self.lbl_give_answer.configure(textvariable=tk.StringVar(value=self.give_answer))
            
            self.error_text = tk.StringVar(value = "Incorrect")
            self.lbl_error.configure(textvariable=self.error_text,
                                        text_color="red")
            
            # turns answer entry box red and locks entry box from changing answer
            self.ent_answer.configure(fg_color="#e69595",
                                    state="disabled")


    # method takes user answer string input from entry box and configures user answer to be comparable
    #   to Question answer
    def check_submit(self):
        print(f"User Answer: |{self.ent_answer.get()}|")                                                  # REMOVE ON FINAL CODE SUBMISSION
        self.user_ansewr = self.ent_answer.get().replace("\"", "")  # removes quotations in answer
        self.user_answer = self.ent_answer.get().replace(" ", "")   # removes spaces in answer
        self.user_answer_int = 0   

        # if self.question is not quadratic or quadratic question has only one root for answer, then run
        if self.question_number < 6 or len(self.question.answer) == 1:
            try:
                self.user_answer_int = int(self.user_answer)
                if self.question_number != 6:
                    self.user_answer = self.user_answer_int
                else:
                    self.user_answer = [self.user_answer]
                self.error_text = tk.StringVar(value = " ")
                self.lbl_error.configure(textvariable=self.error_text,
                                            text_color="red")
                self.input_equals_answer()

            except ValueError:
                if self.user_answer == "":
                    self.error_text = tk.StringVar(value = "Please enter an answer.")
                else:
                    self.error_text = tk.StringVar(value = "Please answer with an integer value.")
                self.lbl_error.configure(textvariable=self.error_text,
                                        text_color="red")
        # else runs if self.question is a quadratic with two roots (not perf square trinomial)
        else:
            self.check_quad_submit()


    # method called for quadratic two root answers (all except perfect square trinomial)
    # method separates user single string answer into a list of two integer values stored as strings
    # after formatting two root answer, user_answer is checked if correct in self.input_equals_answer()
    def check_quad_submit(self):
        # index of "and" in user answer for quadratic question. The "and" separates the roots in answer.
        # -1 is just a placeholder value for no index of "and"
        and_idx = -1 

        user_new_answer_list = []   # list of correct roots submitted by user
        continue_checking = True
        if self.user_answer == "":
            self.error_text = tk.StringVar(value = "Please enter an answer.")
            continue_checking = False

        if continue_checking:
            try:
                and_idx = self.user_answer.index("and")

                # first user root answer is substring until "and"
                num1 = self.user_answer[0 : and_idx]
                # second user root answer is substring until "and"
                num2 = self.user_answer[and_idx + len("and") : len(self.user_answer)]
                user_answer_list = [num1, num2]

                # for loop iterates over both roots in Question object and checks if either equals a
                # string in user's submitted roots. If so, they are added to a list of correct roots.
                for i in self.question.answer:
                    for j in user_answer_list:
                        if i == j:
                            user_new_answer_list.append(i)
                            user_answer_list.pop(user_answer_list.index(j))
                self.user_answer = user_new_answer_list
            except ValueError:  # if user fails to put "and" in two root answer, answer is incorrect
                self.user_answer = "incorrect answer"

        self.input_equals_answer()  # checks if user two root answer is correct

    # method changes visible next button from unclickable next button to clickable next button
    def open_next_btn(self):
        self.btn_next_locked.pack_forget()
        self.btn_next.pack(padx=20,
                           pady=20)
    # method changes visible next button from clickable next button to unclickable next button
    def close_next_btn(self):
        self.btn_next.pack_forget()
        self.btn_next_locked.pack(padx=20,
                                  pady=20)
    
    # method displays a new screen after all questions with the user's number of correct answers
    def disp_results(self):
        self.upper_frame.pack_forget() # removes upper portion of question screen
        self.answer_area.pack_forget() # removes input answer area of question screen
        self.btn_next.pack_forget()    # removes next button of question screen

        # lbl_results is title at top of results screen 
        self.lbl_results = ctk.CTkLabel(master=self.master_root,
                                        textvariable=tk.StringVar(value="Math Test Results"),
                                        font=("Bauhaus 93", 45))
        self.lbl_results.pack(pady=15)

        #lbl_questions_correct displays the number of questions (out of 5) the user got correct
        questions_correct_str = f"You got {self.correct_answers} out of 5\nquestions correct!"
        self.lbl_questions_correct = ctk.CTkLabel(master=self.master_root,
                                                  textvariable=tk.StringVar(value=questions_correct_str),
                                                  font=("Cascadia Code Bold", 30))
        self.lbl_questions_correct.pack(pady = 60)
        


# function called by MathTest submit button (instance attribute self.btn_submit) when clicked to call 
# check_submit() to submit/check the user's answer provided in the entry box and lock entry box answer
def submit_answer():
    test.btn_submit.configure(hover_color = '#3B8ED0')
    test.check_submit()
    

# function called by clickable unlocked next button when clicked
# function
def next_question():
    test.btn_submit.configure(hover_color = '#36719F')
    try:    # checks if user is done with all questions. if index error, then done

        # statement only to cause index error
        try_placeholder_var = test.question_list.index(test.question) + 1

        test.lbl_give_answer.configure(textvariable=tk.StringVar(value=""))     # clears lbl_give_answer
        test.question_sequencer()
    except: # index error means user is done with all questions, and disp_results() method called
        print(f"You got {test.correct_answers} out of 5 questions correct!")                              # REMOVE ON FINAL SUBMISSION
        test.disp_results()
        

# function called by btn_start to clear Math Test introduction screen and start test
def start_test():
    test.intro_frame.pack_forget()

    test.upper_frame.pack()
    test.gen_answer_area()



def main():
    app = App()                 # top level customtkinter window

    # MathTest object is global to allow customtkinter button widget "command" functions to 
    global test
    test = MathTest(app)
    test.disp_intro_screen()    # calls disp_intro_screen() to start first user interaction with program

    app.mainloop()              # customtkinter mainloop (its purpose and function is same as tkinter)

if __name__ == "__main__":
    main()
