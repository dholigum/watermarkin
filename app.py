import streamlit as st
import os 
from io import BytesIO
from PIL import Image, ImageOps
from pillow_heif import register_heif_opener

class heic_to_img_converter():
    
    def __init__(self) -> None:
        register_heif_opener()
        self.uploaded_files = ""
        self.bytes_data = ""
        self.upload_file()     
    
    def upload_file(self):
        self.uploaded_logo = st.file_uploader("Unggah file logo sebagai watermark", accept_multiple_files= False)

        self.uploaded_files = st.file_uploader("Unggah gambar yg ingin di-watermark", accept_multiple_files= True)     
        if self.uploaded_files: 
            if not os.path.exists('converted_images'):
                os.makedirs('converted_images')
            
            st.write("Gambar yg akan diwatermark:")
            for uploaded_file in self.uploaded_files:
                self.bytes_data = uploaded_file.read()    
                st.write("Nama File:", uploaded_file.name)
            
            if st.button("Watermark Gambar"):
                self.watermarking_image()
            
        else:
            st.write("Tolong unggah gambar logo dan gambar yg ingin di-watermark")
             
            
    def watermarking_image(self):
        self.original_logo = Image.open(self.uploaded_logo)
        # Check if the logo has an alpha channel
        if self.original_logo.mode == 'RGBA':
            self.logo_mask_original = self.original_logo.split()[3]
        else:
            self.logo_mask_original = None
            
        for uploaded_file in self.uploaded_files:
            self.file_name = uploaded_file.name.lower()
            if self.file_name.endswith('.heic'):
                
                with Image.open(uploaded_file) as heif_file:
                    self.new_file_name = os.path.basename(self.file_name).replace('.heic','.jpg') 
                    self.image = heif_file.convert('RGB')

            else:
                self.new_file_name = os.path.basename(self.file_name)
                self.image = Image.open(uploaded_file)
                self.image = ImageOps.exif_transpose(self.image)

            self.scale = 50
            self.position = 'bottomleft'
            self.padding = 50
                
            imageWidth, imageHeight = self.image.size
            shorter_side = min(imageWidth, imageHeight)
            new_logo_width = int(shorter_side * self.scale/100)
            logo_aspect_ratio = self.original_logo.width / self.original_logo.height
            new_logo_height = int(new_logo_width / logo_aspect_ratio)

            # Resize the logo and its mask
            logo = self.original_logo.resize((new_logo_width, new_logo_height))
            if self.logo_mask_original:
                logo_mask = self.logo_mask_original.resize((new_logo_width, new_logo_height))
            else:
                logo_mask = None

            paste_x, paste_y = 0, 0

            if self.position == 'topleft':
                paste_x, paste_y = self.padding, self.padding
            elif self.position == 'topright':
                paste_x, paste_y = imageWidth - new_logo_width - self.padding, self.padding
            elif self.position == 'bottomleft':
                paste_x, paste_y = self.padding, imageHeight - new_logo_height - self.padding
            elif self.position == 'bottomright':
                paste_x, paste_y = imageWidth - new_logo_width - self.padding, imageHeight - new_logo_height - self.padding
            elif self.position == 'center':
                paste_x, paste_y = (imageWidth - new_logo_width) // 2, (imageHeight - new_logo_height) // 2

            try:
                self.image.paste(logo, (paste_x, paste_y), logo_mask)
            except Exception as e:
                print(f"An error occurred: {e}")
            
            # self.new_file_path = os.path.abspath(os.path.join('converted_images', self.new_file_name))
            if self.image.mode == 'RGBA':
                self.image = self.image.convert('RGB')

            with BytesIO() as f:
                self.image.save(f, format='JPEG')
                data = f.getvalue()
            
            st.image(self.image, caption=self.new_file_name)
            # st.download_button(label='Download',data=data,file_name=self.new_file_name)

        
        st.write("Semua gambar sudah di watermark, Yey!")
        
                    
abc = heic_to_img_converter()
