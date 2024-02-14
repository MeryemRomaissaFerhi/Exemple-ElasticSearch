import React from "react";
import { FaSearch } from "react-icons/fa";


const Searchbar = () => {
    return ( 
        <form className="w-[50%] relative m-4" action="">
            <div className="relative ">
                <input type="search" placeholder="Recherche.." className="w-full p-3 rounded-full bg-white outline-none border border-[#D5DD18]" />
                <button className="absolute right-1 top-1/2 -translate-y-1/2 p-3 bg-[#D5DD18] rounded-full">
                 <FaSearch className="text-white"/>
                </button>
            </div>

        </form>
     );
}
 
export default Searchbar;