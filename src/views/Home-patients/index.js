import React from 'react';
import Button from '../../components/Button';
import Images from '../../assets/images';
import Icons from '../../assets/icons';

const HomePatients = () => {
    return (
        <div className='mainContainer'>
                <div className='homeContent'>
                    <div className='projectDescription'>
                        <h1>Renal Spectra</h1>
                        <p>Clasificación del estado renal a través de la medición y análisis de Creatinina en muestras.</p>
                        <Button icon={Icons.arrowRight} text='Ingresar'/>
                    </div>
                    <img src={Images.medicalWoman}/>
                </div>
        </div>
    )
}

export default HomePatients;