from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.core.clipboard import Clipboard
import random

class RSADecryptApp(App):
    length = 0

    def build(self):
        Window.size = (1000, 600)
        self.n, self.e, self.d, self.phi_n = 0, 0, 0, 0
        self.decrypted_message = ""

        self.bits_entry = TextInput(multiline=False, hint_text='Number of bits for encryption', height=50, size_hint=(None, None), size=(250, 100), pos_hint={'center_x': 0.5})
        self.message_entry = TextInput(multiline=True, hint_text='Message to encrypt or encrypted message', height=50, size_hint=(None, None), size=(250, 100), pos_hint={'center_x': 0.5})
        
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
        
        self.generate_key_button = Button(text='Generate Key', on_press=self.generate_key_click, size_hint=(None, 1), size=(200, 50))
        self.encrypt_button = Button(text='Decrypt', on_press=self.decrypt_click, size_hint=(None, 1), size=(200, 50))
        self.copy_button = Button(text='Copy Public Key', on_press=self.copy_public_key, size_hint=(None, 1), size=(200, 50))
        self.copy_decrypted_button = Button(text='Copy Decrypted Message', on_press=self.copy_decrypted_message, size_hint=(None, 1), size=(250, 50))

        main_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        title_label = Label(text='RSA Decryption', font_size='24sp', size_hint_y=None, height=150)
        input_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None, height=200)
        input_layout.add_widget(Label(text='Number of bits for encryption:', valign='middle',  font_size='16sp'))
        input_layout.add_widget(self.bits_entry)
        input_layout.add_widget(Label())
        input_layout.add_widget(Label(text='Encrypted message:', valign='middle',  font_size='16sp'))
        input_layout.add_widget(self.message_entry)
        input_layout.add_widget(Label())

        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        button_layout.add_widget(Label())
        button_layout.add_widget(self.generate_key_button)
        button_layout.add_widget(self.encrypt_button)
        button_layout.add_widget(self.copy_button)
        button_layout.add_widget(self.copy_decrypted_button)
        button_layout.add_widget(Label())
                
        main_layout.add_widget(Label())  
        main_layout.add_widget(title_label)
        main_layout.add_widget(input_layout)
        main_layout.add_widget(button_layout)
        main_layout.add_widget(self.result_label)
        main_layout.add_widget(Label())  

        return main_layout

    def is_prime(self, num):
        for divisor in range(2, num):
            if num % divisor == 0:
                return False
        return True

    def generate_prime(self, bits):
        while True:
            num = random.getrandbits(bits)
            if self.is_prime(num) and num != 0:
                return num

    def extended_gcd(self, a, b):
        if a == 0:
            return b, 0, 1
        else:
            g, x, y = self.extended_gcd(b % a, a)
            return g, y - (b // a) * x, x

    def modinv(self, a, m):
        g, x, y = self.extended_gcd(a, m)
        if g != 1:
            raise Exception('No modular inverse')
        else:
            return x % m


    def decrypt_click(self, instance):
        message = self.message_entry.text
        try:
            self.private_key = (self.n, self.d)
            decrypted_message = self.rsa_decrypt(eval(message), self.private_key)

            # Quebra a mensagem em linhas de até 50 caracteres e exibe na label
            decrypted_message_lines = [decrypted_message[i:i+50] for i in range(0, len(decrypted_message), 50)]
            formatted_message = '\n'.join(decrypted_message_lines)
            self.decrypted_message = decrypted_message
            if(len(message) > 200):
                self.result_label.text = f"Decrypted Message:\n{formatted_message[0:200]}...\n Complete decrypted message is too long. Complete message copy to clipboard!"
                
            else:
                self.result_label.text = f"Decrypted Message:\n{formatted_message}"
            

        except Exception as e:
            if(not self.d):
                self.result_label.text = f"Error: Key not found."
            else:
                self.result_label.text = f"Error: {str(e)}"

    def rsa_decrypt(self, message, private_key):
        n, d = private_key
        decrypted_message = [pow(byte, d, n) for byte in message[:-1]]
        partial_decryption = ''.join(chr(char) for char in decrypted_message)
        
        last_byte = pow(message[-1], d, n)
        last_char = chr(last_byte)

        full_decrypted_message = partial_decryption + last_char
        return full_decrypted_message

    # def rsa_decrypt(self, message, private_key):
    #         n, d = private_key
    #         decrypted_message = [chr(pow(i, d, n)) for i in message]
    #         return ''.join(decrypted_message)
    

    def generate_keys(self, bits):
        p = self.generate_prime(bits)
        q = self.generate_prime(bits)

        self.n = p * q
        self.phi_n = (p - 1) * (q - 1)

        self.e = 65537
        self.d = self.modinv(self.e, self.phi_n)

        return p, q, self.n, self.phi_n, self.e, self.d
      
    def generate_key_click(self, instance):
        bits = int(self.bits_entry.text)
        _, _, self.n, _, _, self.d = self.generate_keys(bits)
        self.result_label.text = f"Public Key (n, e): {self.n, self.e}"
        RSADecryptApp.length = len(self.result_label.text)
        print(self.n, ", ", self.e)  

    def copy_public_key(self, instance):
        Clipboard.copy(f"{self.n}, {self.e}")
        print("Public Key copied to clipboard!")

    def copy_decrypted_message(self, instance):
        # decrypted_message = self.result_label.text.split('Decrypted Message: ')[-1]
        Clipboard.copy(self.decrypted_message)
        print("Decrypted message copied to clipboard!")

if __name__ == '__main__':
    RSADecryptApp().run()
