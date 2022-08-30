import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from pathlib import Path
from tkinter import filedialog


class MainForm(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(fill=BOTH, expand=YES)

        self.photoimages = []
        self.start = False
        self.file = None

        self.source_file = ttk.StringVar()
        self.destination_path = ttk.StringVar()
        self.afterid = ttk.StringVar()

        self.button_action = None

        self.associate_icons()
        self.create_buttonbar()
        self.create_path_frame()

    def associate_icons(self):
        image_files = {
            'play': 'icons8-reproduzir-24.png',
            'stop': 'icons8-parar-24.png',
            'settings-light': 'icons8-configuracoes-24.png',
            'refresh': 'icons8-actualizar-24.png'
        }

        imgpath = Path(__file__).parent / '../assets'
        for key, val in image_files.items():
            _path = imgpath / val
            self.photoimages.append(ttk.PhotoImage(name=key, file=_path))

    def create_buttonbar(self):
        buttonbar = ttk.Frame(self, style='primary.TFrame')
        buttonbar.pack(fill=X, pady=1, side=TOP)

        self.button_action = ttk.Button(
            master=buttonbar, text='Iniciar',
            image='play',
            compound=LEFT,
            command=self.on_action
        )
        self.button_action.pack(side=LEFT, ipadx=5, ipady=5, padx=(1, 0), pady=1)

        btn = ttk.Button(
            master=buttonbar,
            text='Configurações',
            image='settings-light',
            compound=LEFT
        )
        btn.pack(side=LEFT, ipadx=5, ipady=5, padx=0, pady=1)

    def create_path_frame(self):
        frame = ttk.Frame(self)
        frame.pack(fill="x", padx=20, pady=15)

        label = ttk.Label(frame, text="Origem")
        label.grid(row=0, column=0, padx=1, sticky=ttk.E)

        path = ttk.Entry(frame, width=50, state="disabled", textvariable=self.source_file)
        path.grid(row=0, column=1, padx=2, sticky=ttk.W)

        btn = ttk.Button(frame, text="Selecionar Arquivo", width=18, bootstyle=(INFO, OUTLINE),
                         command=self.on_browse_file)
        btn.grid(row=0, column=2, padx=2)

        label = ttk.Label(frame, text="Destino")
        label.grid(row=1, column=0, padx=1, pady=(20, 0), sticky=ttk.E)

        path = ttk.Entry(frame, width=50, state="disabled", textvariable=self.destination_path)
        path.grid(row=1, column=1, padx=2, pady=(20, 0), sticky=ttk.W)

        btn = ttk.Button(frame, text="Selecionar Pasta", width=18, bootstyle=(INFO, OUTLINE),
                         command=self.on_browse_folder)
        btn.grid(row=1, column=2, padx=2, pady=(20, 0), sticky=ttk.W)

        label = ttk.Label(frame, text="Tempo Sincronismo")
        label.grid(row=2, column=0, padx=1, pady=(20, 0), sticky=ttk.E)

        path = ttk.Entry(frame, width=15)
        path.grid(row=2, column=1, padx=2, pady=(20, 0), sticky=ttk.W)

    def on_browse_folder(self):
        path = filedialog.askdirectory(initialdir=r'c:\\', title="Selecionar Pasta")
        if path:
            self.destination_path.set(path)

    def on_browse_file(self):
        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
        )
        filename = filedialog.askopenfilename(title='Selecionar Arquivo', initialdir='c:', filetypes=filetypes)
        if filename:
            self.source_file.set(filename)

    def on_action(self):
        file = self.source_file.get()
        self.file = file.split("/")[-1]

        if not self.start:
            if self.validate():
                self.change_button_action_to_start(False)
                self.start = True
                self.after(0, self.loop)
        else:
            self.change_button_action_to_start(True)
            self.start = False
            self.after_cancel(self.afterid.get())

    def loop(self):
        print(self.destination_path.get() + "/" + self.file)
        self.afterid.set(self.after(5000, self.loop))

    def validate(self):
        return True

    def change_button_action_to_start(self, value: bool) -> None:
        if value:
            self.button_action['image'] = 'play'
            self.button_action['text'] = 'Iniciar'
        else:
            self.button_action['image'] = 'stop'
            self.button_action['text'] = 'Parar'
