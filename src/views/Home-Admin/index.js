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
                        <div className='containerButtons'>
                            <Button icon={Icons.plus} text='Nuevo Paciente'/>
                            <Button icon={Icons.magnifyingGlass} text='Buscar'/>
                        </div>
                    </div>
                    <img src={Images.medicalWoman}/>
                </div>
        </div>
    )
}

export default HomePatients;