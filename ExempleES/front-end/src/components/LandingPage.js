import React, { useState } from "react";
import bg from '../images/bg.jpg';
import { FaSearch } from "react-icons/fa";
import { ReactTyped } from "react-typed";
import { useNavigate } from "react-router-dom";

const LandingPage = () => {
    const nav = useNavigate();

    const [motcle, setMotcle] = useState('');
    
    const handleChange = (e) => {
        setMotcle(e.target.value); 
    }
    const [aut, setAut] = useState({
        nom: 'Aut',
        prenom: 'prAut'
    });
    
   
    
    const handleSubm = async (e) => {

        e.preventDefault();
        try {
            const response = await fetch(`http://127.0.0.1:8000/search/${motcle}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                const result = await response.json();
                console.log(result);
                nav(`/Articles?&Formarticle=${encodeURIComponent(JSON.stringify(result))}`);
                console.log(result);
                // Handle successful signup, maybe redirect the user to another page
            } else {
                // Handle error response from the server
                console.error('search failed');
                alert('erreur dans la récuperation des articles depuis Elasticsearch');
            }
        } catch (error) {
            console.error('erreur dans la récuperation des articles depuis Elasticsearch:', error);
        }
    }


    return (
        <div>
         
<<<<<<< HEAD
            <div className='w-full h-screen '>
=======
            <div className='w-full h-screen text-white'>
                <img className="top-0 left-0 w-full h-full object-cover" src={bg} alt="bg" />
>>>>>>> 1523131fca2d53d4512ee208158ba5c91b1ea24e
                <div className="bg-black/70 absolute top-0 left-0 w-full h-screen" />

                <div className="absolute top-0 h-full w-full flex flex-col justify-center">
                    <div className="text-center">
                        <div className='py-24'></div>
<<<<<<< HEAD
                        <h1 className="md:text-7xl sm:text-6xl text-4xl font-bold md:py-4 text-white ">Articles scientifique</h1>

                        <div className="relative flex justify-center items-center py-4">
                            <p className="absolute md:text-3xl sm:text-xl text-xs text-white    "> Une fenêtre sur le monde du savoir</p>
                        </div>
                        <div className="py-20 flex justify-center">
=======
                        <h1 className="md:text-7xl sm:text-6xl text-4xl font-bold md:py-4">Articles scientifique</h1>

                        <div className="relative flex justify-center items-center py-4">
                            <p className="absolute md:text-3xl sm:text-xl text-xs"> Une fenêtre sur le monde du savoir</p>
                        </div>
                        <div className="py-20 flex justify-center text-black">
>>>>>>> 1523131fca2d53d4512ee208158ba5c91b1ea24e
                            <form onSubmit={handleSubm} className="w-[50%] relative m-4" action="">
                                <div className="relative ">
                                    <input type="search" value={motcle} onChange={handleChange} placeholder="Recherche.." className="w-full p-3 rounded-[20px]  bg-white outline-none border border-[#2D82B5]" />
                                    <button type="submit" className="absolute right-1 top-1/2 -translate-y-1/2 p-3 bg-[#2D82B5] rounded-[20PX]">
                                        <FaSearch className="text-white" />
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default LandingPage;
