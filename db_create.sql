-- Last modification date: 2022-05-01 03:12:50.869

-- tables
-- Table: Cita
CREATE TABLE Cita (
    Id_Cita int  NOT NULL,
    id_paciente int  NOT NULL,
    id_doctor int  NOT NULL,
    FechaReserva timestamp  NOT NULL,
    FechaConsulta timestamp  NOT NULL,
    CONSTRAINT Cita_pk PRIMARY KEY  (Id_Cita)
);

-- Table: Consulta
CREATE TABLE Consulta (
    Id_Consulta int  NOT NULL,
    Id_Cita int  NOT NULL,
    Descripcion Varchar(200)  NOT NULL,
    MontoTotal decimal(6,2)  NOT NULL,
    Id_Servicio int  NOT NULL,
    CONSTRAINT Consulta_pk PRIMARY KEY  (Id_Consulta)
);

-- Table: Consulta_Medicina_Receta
CREATE TABLE Consulta_Medicina_Receta (
    Id_Receta int  NOT NULL,
    Id_Med int  NOT NULL,
    "Desc" Varchar(60)  NOT NULL,
    Id_Consulta int  NOT NULL,
    CONSTRAINT Consulta_Medicina_Receta_pk PRIMARY KEY  (Id_Receta)
);

-- Table: Especialidad
CREATE TABLE Especialidad (
    Id_Especialidad int  NOT NULL,
    Especialidad Varchar(60)  NOT NULL,
    CONSTRAINT Especialidad_pk PRIMARY KEY  (Id_Especialidad)
);

-- Table: Laboratorio
CREATE TABLE Laboratorio (
    Id_Lab int  NOT NULL,
    Nombre Varchar(50)  NOT NULL,
    CONSTRAINT Laboratorio_pk PRIMARY KEY  (Id_Lab)
);

-- Table: Medicina
CREATE TABLE Medicina (
    Id_Med int  NOT NULL,
    Nombre int  NOT NULL,
    Tipo Varchar(50)  NOT NULL,
    CONSTRAINT Medicina_pk PRIMARY KEY  (Id_Med)
);

-- Table: Medico
CREATE TABLE Medico (
    id_personaAI int  NOT NULL,
    Fecha_Contrato date  NOT NULL,
    usuario varchar(30)  NOT NULL,
    pass varchar(30)  NOT NULL,
    Contratado bit  NOT NULL,
    Correo_Instit varchar(64)  NOT NULL,
    CONSTRAINT Medico_pk PRIMARY KEY  (id_personaAI)
);

-- Table: Medico_Especialidad
CREATE TABLE Medico_Especialidad (
    Id_Med_Esp int  NOT NULL,
    Id_Especialidad int  NOT NULL,
    Fecha_Titulo date  NOT NULL,
    Medico_id_personaAI int  NOT NULL,
    CONSTRAINT Medico_Especialidad_pk PRIMARY KEY  (Id_Med_Esp)
);

-- Table: Paciente
CREATE TABLE Paciente (
    id_personaAI int  NOT NULL,
    Correo_Paciente Varchar(100)  NOT NULL,
    usuario varchar(30)  NOT NULL,
    pass varchar(30)  NOT NULL,
    alergias varchar(50)  NOT NULL,
    enfermedades_base varchar(50)  NOT NULL,
    CONSTRAINT Paciente_pk PRIMARY KEY  (id_personaAI)
);

-- Table: PagosConsulta
CREATE TABLE PagosConsulta (
    Id_PagoConsulta int  NOT NULL,
    Id_Consulta int  NOT NULL,
    Monto int  NOT NULL,
    CONSTRAINT PagosConsulta_pk PRIMARY KEY  (Id_PagoConsulta)
);

-- Table: PagosReserva
CREATE TABLE PagosReserva (
    Id_Pago int  NOT NULL,
    Monto decimal(6,2)  NOT NULL,
    Id_Tarjeta int  NOT NULL,
    Id_Cita int  NOT NULL,
    CONSTRAINT PagosReserva_pk PRIMARY KEY  (Id_Pago)
);

-- Table: Persona
CREATE TABLE Persona (
    id_personaAI int  NOT NULL,
    CI int  NOT NULL,
    Nombre Varchar(60)  NOT NULL,
    Apellido Varchar(60)  NOT NULL,
    Tel int  NOT NULL,
    FechaNacimiento date  NOT NULL,
    CONSTRAINT Persona_pk PRIMARY KEY  (id_personaAI)
);

-- Table: Rayos_X
CREATE TABLE Rayos_X (
    Id_Rayos int  NOT NULL,
    Tipo Varchar(60)  NOT NULL,
    Id_Consulta int  NOT NULL,
    Id_Lab int  NOT NULL,
    CONSTRAINT Rayos_X_pk PRIMARY KEY  (Id_Rayos)
);

-- Table: Servicio
CREATE TABLE Servicio (
    Id_Servicio int  NOT NULL,
    NombreServicio Varchar(60)  NOT NULL,
    CONSTRAINT Servicio_pk PRIMARY KEY  (Id_Servicio)
);

-- Table: Tarjeta
CREATE TABLE Tarjeta (
    Id_Tarjeta int  NOT NULL,
    FechaCaducidad date  NOT NULL,
    CVC int  NOT NULL,
    Paciente_id_personaAI int  NOT NULL,
    CONSTRAINT Tarjeta_pk PRIMARY KEY  (Id_Tarjeta)
);

-- End of file.
