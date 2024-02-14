import React, { useEffect, useState } from "react";
import { FaSearch } from "react-icons/fa";
import { IoFilter } from "react-icons/io5";
import { useNavigate, useLocation } from "react-router-dom";
import { AiOutlineClose } from 'react-icons/ai'
import { FaStar } from "react-icons/fa";
const Articles = () => {
    const location = useLocation();

    const [filterKey, setfilterkey] = useState('');

    const handleChange = (e) => {
        setfilterkey(e.target.value); 
    }
    const [isArcticleDetPageVisible, setLoginPageVisible] = useState(false);
    let nav = useNavigate();

    const [filtrer, setPgfiltre] = useState(false);


    

    const searchParams = new URLSearchParams(location.search);
    const FormarticleString = searchParams.get('Formarticle');
    const Formarticle = FormarticleString ? JSON.parse(FormarticleString).results : [];
    
    console.log('in Articles');
    console.log(Formarticle);

    const handlefilter = () => {
        setPgfiltre(!filtrer);
    }
    const handleFilterAuteur = async (e) => {

        e.preventDefault();
        try {
            const response = await fetch(`http://127.0.0.1:8000/filter_by_author/${filterKey}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                const result = await response.json();
                console.log(result);
                Formarticle = result;
                // Handle successful signup, maybe redirect the user to another page
            } else {
                // Handle error response from the server
                console.error('filter failed');
                alert('erreur dans le filtrage');
            }
        } catch (error) {
            console.error('erreur dans le filtrage:', error);
        }
    }

    const handleFilterInstitus = async (e) => {

        e.preventDefault();
        try {
            const response = await fetch(`http://127.0.0.1:8000/filter_by_institution/${filterKey}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                const result = await response.json();
                console.log(result);
                Formarticle = result;
                // Handle successful signup, maybe redirect the user to another page
            } else {
                // Handle error response from the server
                console.error('filter failed');
                alert('erreur dans le filtrage');
            }
        } catch (error) {
            console.error('erreur dans le filtrage:', error);
        }
    }
    const handleFiltermotcle = async (e) => {

        e.preventDefault();
        try {
            const response = await fetch(`http://127.0.0.1:8000/filter_by_keyword/${filterKey}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                const result = await response.json();
                console.log(result);
                Formarticle = result;
                // Handle successful signup, maybe redirect the user to another page
            } else {
                // Handle error response from the server
                console.error('filter failed');
                alert('erreur dans le filtrage');
            }
        } catch (error) {
            console.error('erreur dans le filtrage:', error);
        }
    }
    const handleFilterPeriod = async (e) => {

        e.preventDefault();
        try {
            const response = await fetch(`http://127.0.0.1:8000/filter_by_publication_date/${filterKey}/${filterKey}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                const result = await response.json();
                console.log(result);
                Formarticle = result;
                // Handle successful signup, maybe redirect the user to another page
            } else {
                // Handle error response from the server
                console.error('filter failed');
                alert('erreur dans le filtrage');
            }
        } catch (error) {
            console.error('erreur dans le filtrage:', error);
        }
    }
    const handleFav = () => {
      
    }
    return (

        <div className="absolute bg-white justify-center h-full w-full text-black z-20">
            <div className="pt-24 pb-3 mx-10 lg:mx-40 border-b-2 border-b-gray-300 flex justify-center items-center">
                <div className="w-[60%] relative m-4 p-3 rounded-full border bg-[#3463c0]/40 " >

                    <div className="relative flex">
                        <form action="">
                            <input type="search"  value={filterKey} onChange={handleChange} placeholder='Filtrer..' className="text-white  placeholder-white border-none outline-none bg-transparent  w-[80%]" />
                        </form>
                        <button className="absolute right-12 top-1/2 -translate-y-1/2 p-2 bg-[#6a6969] rounded-full">
                            <IoFilter onClick={handlefilter} className="text-white" size={20} />
                        </button>
                        <button className="absolute right-1 top-1/2 -translate-y-1/2 p-2 bg-[#6a6969] rounded-full">
                            <FaSearch className="text-white" size={20} />
                        </button>
                    </div>
                </div>
                <div>
                    {filtrer && (
                        <div className="fixed flex left-0 top_0 bottom-0 w-full h-full bg-black/40 justify-center items-center z-10">
                            <div className="fixed top-[30%]  w-full lg:w-1/2 md:w-[30%] h-[55%] border-r border-r-gray-900 bg-[#3463c0] rounded-3xl ease-in-out duration-500 p-4">
                                <AiOutlineClose className=" text-white cursor-pointer" onClick={handlefilter} size={20} />
                                <div className='flex py-4 px-6 border-b border-gray-300 items-center'>
                                    <h1 className='px-3 text-2xl text-white'> Filtrage selon: </h1>
                                </div>
                                <div className='text-white font-medium flex flex-col py-10 px-6'>
                                    <div className='flex items-center py-2'>
                                        <button onClick={handleFilterAuteur} className='px-2 text-xl'>Auteur</button>
                                    </div>
                                    <div className='flex items-center py-2'>
                                        <button onClick={handleFilterInstitus} className='px-2 text-xl'>Institutions</button>
                                    </div>
                                    <div className='flex items-center py-2'>
                                        <button onClick={handleFiltermotcle} className='px-2 text-xl'>Mot clés</button>
                                    </div>
                                    <div className='flex items-center py-2'>
                                        <button onClick={() => handleFilterPeriod} className='px-2 text-xl'>Période</button>
                                    </div>
                                    
                                </div>
                            </div>
                        </div>
                    )}

                </div>
            </div>

            <ul className=" text-black py-6 mx-10  border-b border-b-gray-300 flex flex-col">

                {Formarticle.length === 0 ? (
                    <div className="text-black py-6 mx-10 lg:mx-40 border-b border-b-gray-300 flex flex-col">
                        <h1 className="font-bold text-xl lg:text-3xl py-3">Pas de résultat trouvé</h1>
                    </div>
                ) : (
                    Formarticle.map((article, index) => (
                        <div className="text-[#3463c0] py-6 mx-10 lg:mx-40 border-b border-b-gray-600 flex flex-col" key={index}>
                            <h1  className="font-bold text-xl lg:text-2xl py-3 cursor-pointer">{article.titre} :</h1>
              
                            <p className="text-black lg:text-2xl py-2">{article.resume ? article.resume : 'pas de résumé.'}</p>
                            <div className="flex">
                                <h3 className="text-[#194c36] lg:text-xl font-semibold">Mots clé : </h3>
                                <p className="text-black px-4 py-1.5">{article.motscles ? article.motscles : 'pas de mot clé!'}</p>
                            </div>
                        </div>
                    ))
                )}
            </ul>
        </div>

    );
}

export default Articles;
