import React from 'react';
import Button from '../../components/Button';
import Icons from '../../assets/icons';
import './add-patient.css';

const AddPatient = () => {
    return (
        <div id="divAddPatient" className='mainContainer'>
            <div className='homeContent'>
                <div className='projectDescription'>
                    <h2>Ingrese la información del paciente:</h2>
                    <form action="/ruta_de_envio" method="post" class='loginForm'>
                        <div className='info-container-row'>
                            <div className='info-container'>
                                <label for="nombre">Nombres:</label>
                                <input type="text" id="nombre" name="nombre" required />
                            </div>
                            <div className='info-container'>
                                <label for="apellidos">Apellidos:</label>
                                <input type="text" id="apellidos" name="apellidos" required />
                            </div>
                        </div>
                        <div className='info-container-row'>
                            <div className='info-container'>
                                <label for="ci">Cédula de Identidad:</label>
                                <input type="text" id="ci" name="ci" required />
                            </div>
                            <div className='info-container'>
                                <label for="fecha_nacimiento">Fecha de Nacimiento:</label>
                                <input type="date" id="fecha_nacimiento" name="fecha_nacimiento" required />
                            </div>
                        </div>
                        <div className='info-container-row'>
                            <div className='info-container'>
                                <label for="peso">Peso (kg):</label>
                                <input type="number" id="peso" name="peso" required />
                            </div>
                            <div className='info-container'>
                                <label for="altura">Altura (m):</label>
                                <input type="number" id="altura" name="altura" required />
                            </div>
                        </div>
                        <div class="radio-container">
                            <label>Género:</label>
                            <div className='optionsContainer'>
                                <div className='info-container'>
                                    <input type="radio" id="masculino" name="genero" value="Masculino" required />
                                    <label className='option' for="masculino">Masculino</label>
                                </div>
                                <div className='info-container'>
                                    <input type="radio" id="femenino" name="genero" value="Femenino" required />
                                    <label className='option' for="femenino">Femenino</label>
                                </div>
                            </div>
                        </div>
                        
                        <div className='containerButtons'>
                            <Button icon={Icons.arrowLeft} text='Cancelar'/>
                            <Button icon={Icons.arrowRight} text='Añadir Paciente'/>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    )
}

export default AddPatient;