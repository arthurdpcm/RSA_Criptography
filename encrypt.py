from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.clipboard import Clipboard

class RSAEncryptApp(App):
    def build(self):
        self.n, self.e, self.d, self.phi_n = 0, 0, 0, 0

        self.public_key_entry = TextInput(multiline=False, hint_text='Enter public key in the format: n, e', height=50, size_hint=(None, None), size=(250, 100), pos_hint={'center_x': 0.5})
        self.message_entry = TextInput(multiline=True, hint_text='Enter message to encrypt', height=50, size_hint=(None, None), size=(250, 100), pos_hint={'center_x': 0.5})

        self.result_label = Label(
            text='',
            font_size='20sp',
            size_hint_y=None,
            valign='top',
            halign='center',
            markup=True,
            padding=[20, 20],
            height=200, 
            text_size=(None, None)  
        )

        self.copy_button = Button(text='Copy Encrypted Message', size_hint=(None, 1), size=(200, 50), on_press=self.copy_encrypted_message)
        self.encrypt_button = Button(text='Encrypt', size_hint=(None, 1), size=(150, 50), on_press=self.encrypt_click)

        self.main_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        title_label = Label(text='RSA Encryption', font_size='24sp', size_hint_y=None, height=150) 
        input_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None, height=200)
        input_layout.add_widget(Label(text='Public Key (n, e):', valign='middle',  font_size='16sp'))
        input_layout.add_widget(self.public_key_entry)
        input_layout.add_widget(Label())
        input_layout.add_widget(Label(text='Message to Encrypt:', valign='middle',  font_size='16sp'))
        input_layout.add_widget(self.message_entry)
        input_layout.add_widget(Label())

        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        button_layout.add_widget(Label()) 
        button_layout.add_widget(self.encrypt_button)
        button_layout.add_widget(self.copy_button)
        button_layout.add_widget(Label())

        self.main_layout.add_widget(Label()) 
        self.main_layout.add_widget(title_label)
        self.main_layout.add_widget(input_layout)
        self.main_layout.add_widget(button_layout)
        self.main_layout.add_widget(self.result_label)
        self.main_layout.add_widget(Label())  
        self.result_label.bind(size=self.on_label_size_change)

        return self.main_layout

    def encrypt_click(self, instance):
        global encrypted_message

        message = self.message_entry.text
        public_key_str = self.public_key_entry.text

        try:
            self.public_key = tuple(map(int, public_key_str.split(',')))
            encrypted_message = self.rsa_encrypt(message, self.public_key)

            if len(encrypted_message) > 30:
                self.result_label.text = f"Encrypted Message: {encrypted_message[:30]}...\n\nComplete encrypted message is too long. Complete message copy to clipboard!"
            else:
                self.result_label.text = f"Encrypted Message: {encrypted_message}"

        except Exception as e:
            self.result_label.text = f"Error: {str(e)}"

    def rsa_encrypt(self, message, public_key):
        n, e = public_key
        encrypted_message = [pow(ord(char), e, n) for char in message]
        print(encrypted_message)
        return encrypted_message

    def copy_encrypted_message(self, message):
        encrypted_message_str = ', '.join(map(str, encrypted_message))
        Clipboard.copy(encrypted_message_str)
        print(f"Encrypted messages copied to clipboard!")

    def on_label_size_change(self, instance, value):

        self.main_layout.height = self.result_label.height + 300 


        self.result_label.text_size = (self.result_label.width, None)

if __name__ == '__main__':
    RSAEncryptApp().run()
