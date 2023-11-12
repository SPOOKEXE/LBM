
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

	widget_frames : list[customtkinter.CTkFrame] = None
	widget_names : list[str] = None
	widget_buttons : list[customtkinter.CTkButton] = None

	def set_frame_visible( self, target_index : int ) -> None:
		for index, frame in enumerate(self.widget_frames):
			if index == target_index:
				self.widget_buttons[index].configure(text_color=("#87B7F3", "#87B7F3"))
				frame.pack()
			else:
				self.widget_buttons[index].configure(text_color=("#DCE4EE", "#DCE4EE"))
				frame.pack_forget()

	def __init__(self, width=800, height=400, topbar_sizey=35):
		super().__init__()

		self.widget_frames = []
		self.widget_names = []
		self.widget_buttons = []

		self.title('Language Brain Model Interface')
		self.resizable(False, False)
		self.geometry("{}x{}".format(width, height))

		FRAME_YSIZE = height - topbar_sizey

		### HOME WIDGET ###
		home_frame = customtkinter.CTkFrame(self, width=width, height=FRAME_YSIZE)
		home_frame.place(rely=topbar_sizey)
		self.widget_frames.append(home_frame)
		self.widget_names.append('HOME')

		### TEXT2AUDIO WIDGET ###
		t2a_frame = customtkinter.CTkFrame(self, width=width, height=FRAME_YSIZE)
		t2a_frame.place(rely=topbar_sizey)
		self.widget_frames.append(t2a_frame)
		self.widget_names.append('TEXT2AUDIO')

		### AUDIO2TEXT WIDGET ###
		a2t_frame = customtkinter.CTkFrame(self, width=width, height=FRAME_YSIZE)
		a2t_frame.place(rely=topbar_sizey)
		self.widget_frames.append(a2t_frame)
		self.widget_names.append('AUDIO2TEXT')

		### LANGUAGE WIDGET ###
		language_frame = customtkinter.CTkFrame(self, width=width, height=FRAME_YSIZE)
		language_frame.place(rely=topbar_sizey)
		self.widget_frames.append(language_frame)
		self.widget_names.append('LANGUAGE')

		### SETTINGS WIDGET ###
		settings_frame = customtkinter.CTkFrame(self, width=width, height=FRAME_YSIZE)
		settings_frame.place(rely=topbar_sizey)
		self.widget_frames.append(settings_frame)
		self.widget_names.append('SETTINGS')

		### TOPBAR ###
		topbar = HorizontalScrollFrame(self, width=width, height=topbar_sizey, orientation="horizontal")
		topbar.configure(fg_color=('gray93', 'gray10'))
		topbar.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
		topbar.pack()
		highest_length = max([ len(v) for v in self.widget_names ])

		# hacky to prevent index from leaking to the next callback setup
		def new_widget_button( index : int, name : str ):
			nonlocal topbar, highest_length
			topbar_button = customtkinter.CTkButton( topbar, text=name, width=highest_length*10, height=topbar_sizey, command=lambda : self.set_frame_visible(index) )
			topbar.add_item(topbar_button)
			self.widget_buttons.append(topbar_button)
		for index, name in enumerate(self.widget_names):
			new_widget_button( index, name )
		self.set_frame_visible( 0 )

def run_display( ) -> None:
	customtkinter.set_appearance_mode('dark')
	customtkinter.set_default_color_theme('dark-blue')
	ui = UI()
	ui.mainloop()

if __name__ == '__main__':
	run_display()
