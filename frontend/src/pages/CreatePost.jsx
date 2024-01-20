import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

import { preview } from "../assets";
import { getRandomPrompt } from "../utils";
import { FormFields, Loader } from "../components";

const CreatePost = () => {
    const navigate = useNavigate();

    const [form, setForm] = useState({
        name: "",
        prompt: "",
        photo: "",
    });

    const [generatingImg, setGeneratingImg] = useState(false);
    const [loading, setLoading] = useState(false);

    const handleChange = (e) =>
        setForm({ ...form, [e.target.name]: e.target.value });

    const handleSurpriseMe = () => {
        const randomPrompt = getRandomPrompt(form.prompt);
        setForm({ ...form, prompt: randomPrompt });
    };

    const generateImage = async () => {
        if (form.prompt) {
            try {
                setGeneratingImg(true);
                const response = await fetch(
                    "https://dalle-hn3a.onrender.com/api/v1/dalle",
                    {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify({
                            prompt: form.prompt,
                        }),
                    }
                );
                const data = await response.json();
              //  console.log(data);
                setForm({ ...form, photo: `data:image/jpeg;base64,${data.photo}` });
            } catch (err) {
                console.log(err);
            } finally {
                setGeneratingImg(false);
            }
        } else {
            alert("Please provide proper prompt");
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (form.prompt && form.photo) {
            setLoading(true);
            try {
                const response = await fetch(
                    "https://dalle-hn3a.onrender.com/api/v1/post",
                    {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify({ ...form }),
                    }
                );
                await response.json();
                // alert("Success");
                navigate("/community");
            } catch (err) {
                console.log(err);
            } finally {
                setLoading(false);
            }
        } else {
            alert("Please generate an image with proper details");
        }
    };

    return (
        <section className="bg-hero min-h-[calc(100vh)]">
            <div className="max-w-7xl bg-hero sm:p-8 px-4 mt-16 m-auto">
            <div>
                <h1 className="font-extrabold text-text text-[42px]">Insert your preferences  </h1>
            </div>

            <form className="mt-2 form" onSubmit={handleSubmit}>
                <div className="flex my-auto flex-col gap-5">
                    <FormFields
                        labelName="The objective"
                        type="text"
                        name="name"
                        placeholder="Enter Your Name"
                        value={form.name}
                        handleChange={handleChange}
                    />
                    <FormFields
                        labelName="The output"
                        type="text"
                        name="name"
                        placeholder="Enter Your Name"
                        value={form.name}
                        handleChange={handleChange}
                    />
                    <FormFields
                        labelName="Scenario"
                        type="text"
                        name="prompt"
                        placeholder="Enter a prompt..."
                        value={form.prompt}
                        handleChange={handleChange}
                        isSurpriseMe
                        handleSurpriseMe={handleSurpriseMe}
                    />


                    <div className="mt-2 flex flex-col">
                        <button
                            type="button"
                            onClick={generateImage}
                            className=" text-black bg-accent font-bold rounded-md text-sm w-full sm:w-auto px-5 py-2.5 text-center"
                        >
                            {generatingImg ? "Generating..." : "Generate Prompt"}
                        </button>
                        <button
                            type="submit"
                            className="mt-3 text-white bg-brand text-black font-bold rounded-md text-sm sm:w-auto px-5 py-2.5 text-center w-full"
                        >
                            {loading ? "Sharing..." : "Use this directly on chatbot"}
                        </button>
                    </div>
                </div>
                <div className="relative form_photo md:m-auto bg-darkgrey border border-darkgrey text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 w-64 p-3 h-64 flex justify-center items-center">
                    {form.photo ? (
                        <img
                            src={form.photo}
                            alt={form.prompt}
                            className="w-full image h-full object-cover"
                        />
                    ) : (
                        <img
                            src={preview}
                            alt="preview"
                            className="w-full image h-full object-contain opacity-50"
                        />
                    )}

                    {generatingImg && (
                        <div className="absolute inset-0 z-0 flex justify-center items-center bg-[rgba(0,0,0,0.5)] rounded-lg">
                            <Loader />
                        </div>
                    )}
                </div>
            </form>
            </div>
        </section>
    );
};

export default CreatePost;
