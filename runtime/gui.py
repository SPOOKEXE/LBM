
import customtkinter

audio2text = None
txt2audio = None
conversation = None

class HorizontalScrollFrame(customtkinter.CTkScrollableFrame):

	def __init__(self, master, **kwargs):
		super().__init__(master, **kwargs)
		self.grid_rowconfigure(0, weight=1)
		self.items_list = []

	def add_item( self, item : customtkinter.CTkBaseClass ) -> None:
		item.grid(row=0, column=len(self.items_list), padx=2)
		self.items_list.append(item)

class UI(customtkinter.CTk):
	# LBM\venv\Lib\site-packages\customtkinter\assets\themes\dark-blue.json

	widget_frames : list[customtkinter.CTkFrame] = []

	def set_frame_visible( self, target_frame : customtkinter.CTkFrame ) -> None:
		for frame in self.widget_frames:
			if frame == target_frame: frame.pack()
			else: frame.pack_forget()

	def __init__(self, width=800, height=400, topbar_sizey=35):
		super().__init__()

		self.title('Language Brain Model Interface')
		self.resizable(False, False)
		self.geometry("{}x{}".format(width, height))

		FRAME_YSIZE = height - topbar_sizey
		frame_titles = []

		### HOME WIDGET ###
		home_frame = customtkinter.CTkFrame(self, width=width, height=FRAME_YSIZE)
		home_frame.place(rely=topbar_sizey)
		self.widget_frames.append(home_frame)
		frame_titles.append('HOME')

		### TEXT2AUDIO WIDGET ###
		t2a_frame = customtkinter.CTkFrame(self, width=width, height=FRAME_YSIZE)
		t2a_frame.place(rely=topbar_sizey)
		self.widget_frames.append(t2a_frame)
		frame_titles.append('TEXT2AUDIO')

		### AUDIO2TEXT WIDGET ###
		a2t_frame = customtkinter.CTkFrame(self, width=width, height=FRAME_YSIZE)
		a2t_frame.place(rely=topbar_sizey)
		self.widget_frames.append(a2t_frame)
		frame_titles.append('AUDIO2TEXT')

		### LANGUAGE WIDGET ###
		language_frame = customtkinter.CTkFrame(self, width=width, height=FRAME_YSIZE)
		language_frame.place(rely=topbar_sizey)
		self.widget_frames.append(language_frame)
		frame_titles.append('LANGUAGE')

		### SETTINGS WIDGET ###
		settings_frame = customtkinter.CTkFrame(self, width=width, height=FRAME_YSIZE)
		settings_frame.place(rely=topbar_sizey)
		self.widget_frames.append(settings_frame)
		frame_titles.append('SETTINGS')

		### TOPBAR ###
		topbar = HorizontalScrollFrame(self, width=width, height=topbar_sizey, orientation="horizontal")
		topbar.configure(fg_color=('gray93', 'gray10'))
		topbar.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
		topbar.pack()
		highest_length = max([ len(v) for v in frame_titles ])
		for frame, name in zip(self.widget_frames, frame_titles):
			topbar_button = customtkinter.CTkButton( topbar, text=name, width=highest_length*10, height=topbar_sizey, command=lambda : self.set_frame_visible(frame) )
			topbar.add_item(topbar_button)

		self.set_frame_visible( home_frame )

def run_display( ) -> None:
	customtkinter.set_appearance_mode('dark')
	customtkinter.set_default_color_theme('dark-blue')
	ui = UI()
	ui.mainloop()

if __name__ == '__main__':
	run_display()
