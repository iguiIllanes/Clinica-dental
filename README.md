# Clinica-dental
Clinica Dental Proyecto final SIS-222 Sistemas de informacion I
## Configuracion de SQL Server
1. Descargar e instalar [Microsoft SQL Server Developer 2019](https://go.microsoft.com/fwlink/?linkid=866662)
2. Descargar e instalar [SQL Server Management Studio 18 (SSMS)](https://aka.ms/ssmsfullsetup)
3. Iniciar SSMS y conectar al servidor de SQL Server
4. Crear la base de datos

  ![Screenshot 2022-05-01 002000](https://user-images.githubusercontent.com/22847626/166132079-5de1022c-7954-4f98-8712-4d8bad815ddb.png)
  ![Screenshot 2022-04-30 230743](https://user-images.githubusercontent.com/22847626/166132085-2a9e9e42-ff01-4a69-b15b-14e11a095e47.png)
  
  * Click derecho en **clinica-dental > New Query** y copiar el contenido de **db_create.sql** y ejecutar

5. Crear usuario para la bd
   
    ![Screenshot 2022-04-30 233632](https://user-images.githubusercontent.com/22847626/166132196-043aac7d-7466-4b7d-a784-d2498b1ff1d7.png)
    ![Screenshot 2022-04-30 233647](https://user-images.githubusercontent.com/22847626/166132199-cdc3bb2a-551d-466c-af2d-72d1e9c2ef20.png)
    
    ```
    LOGIN NAME: clinica-user
    PASSWORD: clinica-user2022
    ```
    
    ![Screenshot 2022-04-30 235526](https://user-images.githubusercontent.com/22847626/166132299-ac0cb6ad-c383-4219-8fcc-f30614165d0d.png)
    ![Screenshot 2022-05-01 003130](https://user-images.githubusercontent.com/22847626/166132330-2009c6f0-63d1-4480-b843-fe770ea0d2e0.png)
    

7. Configurar inicio de sesion en SQL Server
   
   ![Screenshot 2022-05-01 000305](https://user-images.githubusercontent.com/22847626/166132347-e5b61431-87cd-4223-be51-6f5d2375a236.png)
   ![Screenshot 2022-05-01 000334](https://user-images.githubusercontent.com/22847626/166132343-4b040ac5-5447-4fbc-b9a3-faa440c54aa0.png)
   
8. Listo!
