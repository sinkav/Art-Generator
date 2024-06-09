import unittest
from tkinter import Tk, Canvas, BooleanVar, Entry
from art_generator import ArtGenerator, save_settings, load_settings

class TestArtGenerator(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.canvas = Canvas(self.root, width=500, height=500)
        self.canvas.pack()
        self.art_gen = ArtGenerator(self.canvas)
        self.num_shapes_entry = Entry(self.root)
        self.num_shapes_entry.insert(0, "10")
        
        self.color_vars = {"red": BooleanVar(value=True), "blue": BooleanVar(value=True)}
        self.shape_type_vars = {
            "rectangle": BooleanVar(value=True), 
            "circle": BooleanVar(value=True), 
            "triangle": BooleanVar(value=True), 
            "polygon": BooleanVar(value=True), 
            "ellipse": BooleanVar(value=True), 
            "line": BooleanVar(value=True)
        }

    def tearDown(self):
        self.root.destroy()

    def test_draw_rectangle(self):
        self.art_gen.draw_rectangle(10, 10, 50, 50, "red")
        items = self.canvas.find_all()
        self.assertEqual(len(items), 1)
        self.assertEqual(self.canvas.itemcget(items[0], "fill"), "red")

    def test_draw_circle(self):
        self.art_gen.draw_circle(100, 100, 30, "blue")
        items = self.canvas.find_all()
        self.assertEqual(len(items), 1)
        self.assertEqual(self.canvas.itemcget(items[0], "fill"), "blue")

    def test_draw_triangle(self):
        self.art_gen.draw_triangle(20, 20, 60, 20, 40, 60, "green")
        items = self.canvas.find_all()
        self.assertEqual(len(items), 1)
        self.assertEqual(self.canvas.itemcget(items[0], "fill"), "green")

    def test_generate_art(self):
        shape_types = ["rectangle", "circle", "triangle", "polygon", "ellipse", "line"]
        colors = ["red", "blue", "green", "yellow", "black"]
        self.art_gen.generate_art(10, shape_types, colors)
        items = self.canvas.find_all()
        self.assertEqual(len(items), 10)

    def test_save_load_settings(self):
        file_path = "test_settings.txt"
        save_settings(file_path, self.num_shapes_entry.get(), self.color_vars, self.shape_type_vars)
        self.num_shapes_entry.delete(0, 'end')
        self.color_vars["red"].set(False)
        self.shape_type_vars["rectangle"].set(False)
        
        load_settings(file_path, self.num_shapes_entry, self.color_vars, [], self.shape_type_vars, [])
        
        self.assertEqual(self.num_shapes_entry.get(), "10")
        self.assertTrue(self.color_vars["red"].get())
        self.assertTrue(self.shape_type_vars["rectangle"].get())

if __name__ == "__main__":
    unittest.main()

