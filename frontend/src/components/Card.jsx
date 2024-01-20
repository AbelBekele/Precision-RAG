import React from "react";
import { download, hero, logo } from "../assets";
import { downloadImage } from "../utils";

const Card = ({ _id, name, prompt, photo }) => {
    return (
        <div className="rounded-xl group relative shadow-card hover:shadow-cardhover card">
            <img
                src={hero}
                alt={prompt}
                className="w-full h-auto object-cover rounded-xl"
            />
            <div className="group-hover:flex flex-col hidden absolute bottom-0 left-0 right-0 max-h-[94.5%] m-2 p-4 bg-accent rounded-md">
                <p className="overflow-y-auto text-sm">
                    <span className="font-bold">Prompt:</span> {prompt}
                </p>
                <div className="flex justify-between items-center mt-2">
                    <div className="flex items-center gap 2">
                        <span className="w-7 h-7 bg-green-500 text-white font-bold rounded-full flex justify-center items-center object-cover text-xs mr-1">
                            {name[0].toUpperCase()}
                        </span>
                        <p className="text-xs font-bold text-gray-black">
                            <span className=" text-sm"></span> {name}
                        </p>
                    </div>

                    <button
                        onClick={() => downloadImage(_id, logo)}
                        className="outline-none border-none bg-trasparent"
                    >
                        {" "}
                        <img src={download} alt="download" className="w-6 h-6 object-contain invert" />{" "}
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Card;
