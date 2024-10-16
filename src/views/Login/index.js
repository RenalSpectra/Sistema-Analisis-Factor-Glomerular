import React, { useState } from 'react';
import Button from '../../components/Button';
import Images from '../../assets/images';
import Icons from '../../assets/icons';
import './login.css';

const Login = () => {
    // Estado para el correo, contraseña y mensaje de error
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    // Definir las credenciales de inicio de sesión
    const validEmail = 'usuario@example.com'; // Cambia esto al correo deseado
    const validPassword = 'contraseña123'; // Cambia esto a la contraseña deseada

    const handleSubmit = (event) => {
        event.preventDefault(); // Evitar el comportamiento predeterminado del formulario

        // Validar las credenciales
        if (email === validEmail && password === validPassword) {
            // Credenciales válidas
            setErrorMessage(''); // Limpiar el mensaje de error
            // Aquí puedes redirigir al usuario o realizar otra acción
            console.log('Inicio de sesión exitoso');
        } else {
            // Credenciales inválidas
            setErrorMessage('Correo electrónico o contraseña incorrectos');
        }
    };

    return (
        <div className='mainContainer' id='LoginPage'>
            <div className='homeContent'>
                <div className='projectDescription'>
                    <h1>Login</h1>
                    <form onSubmit={handleSubmit} className='loginForm'>
                        <div className='info-container'>
                            <label htmlFor="email">Correo Electrónico:</label>
                            <input 
                                type="email" 
                                id="email" 
                                name="email" 
                                required 
                                value={email} 
                                onChange={(e) => setEmail(e.target.value)} 
                            />
                        </div>
                        <div className='info-container'>
                            <label htmlFor="password">Contraseña:</label>
                            <input 
                                type="password" 
                                id="password" 
                                name="password" 
                                required 
                                value={password} 
                                onChange={(e) => setPassword(e.target.value)} 
                            />
                        </div>
                        <div className="checkbox-container">
                            <input type="checkbox" id="recordar" name="recordar" />
                            <label htmlFor="recordar">Recordarme</label>
                        </div>
                        <div className='containerButtons'>
                            <Button icon={Icons.arrowRight} text='Ingresar' />
                            <Button icon={Icons.arrowLeft} text='Volver' />
                        </div>
                        {/* Mensaje de error */}
                        {errorMessage && <div className="error-message">{errorMessage}</div>}
                    </form>
                </div>
                <img src={Images.medicalWoman} alt="Medical Woman" />
            </div>
        </div>
    );
};

export default Login;
