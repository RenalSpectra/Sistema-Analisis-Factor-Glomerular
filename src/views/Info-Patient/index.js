import React from 'react';
import Button from '../../components/Button';
import Icons from '../../assets/icons';
import './info-patient.css';

const AddPatient = () => {
    return (
        <div id="divInfoPatient" className='mainContainer'>
            <div className='homeContent'>
                <div className='infoPatientContainer'>
                    <h2>Información de paciente:</h2>
                    <form action="/ruta_de_envio" method="post" id='dataShowed'>
                        <div className='info-container-row'>
                            <div className='info-container'>
                                <label for="nombre">Nombres:</label>
                                <p>Luis Alberto</p>
                            </div>
                            <div className='info-container'>
                                <label for="apellidos">Apellidos:</label>
                                <p>López Vega</p>
                            </div>
                        </div>
                        <div className='info-container-row'>
                            <div className='info-container'>
                                <label for="ci">Cédula de Identidad:</label>
                                <p>5278670</p>
                            </div>
                            <div className='info-container'>
                                <label for="fecha_nacimiento">Fecha de Nacimiento:</label>
                                <p>13/03/1990</p>
                            </div>
                        </div>
                        <div className='info-container-row'>
                            <div className='info-container'>
                                <label for="peso">Peso (kg):</label>
                                <p>85.5</p>
                            </div>
                            <div className='info-container'>
                                <label for="altura">Altura (m):</label>
                                <p>1.75</p>
                            </div>
                        </div>
                        <div class="radio-container">
                            <label>Género:</label>
                            <p>Masculino</p>
                        </div>
                        
                        <div className='containerButtons'>
                            <Button icon={Icons.arrowRight} text='Modificar'/>
                            <Button icon={Icons.trendUp} text='Análisis'/>
                            <Button icon={Icons.arrowRight} text='Eliminar'/>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    )
}

export default AddPatient;