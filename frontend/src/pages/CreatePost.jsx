import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

import { preview } from "../assets";
import { getRandomPrompt } from "../utils";
import { FormFields, Loader } from "../components";

const CreatePost = () => {
    const navigate = useNavigate();

    const [form, setForm] = useState({
        objective: "",
        output: "",
        scenario: "",
    });

    const [generatingprompt, setGeneratingprompt] = useState(false);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(""); // Add this line
    const [accuracy, setAccuracy] = useState(null); // Add this line


    const handleChange = (e) =>
        setForm({ ...form, [e.target.name]: e.target.value });

    const handleSurpriseMe = () => {
        const randomPrompt = getRandomPrompt(form.scenario);
        setForm({ ...form, scenario: randomPrompt });
    };

    const generatePrompt = async () => {
        if (form.scenario) {
            try {
                setGeneratingprompt(true);
                const response = await fetch("http://192.168.137.236:8000/generate", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        num_test_output: "8",
                        objective: form.objective,
                        output: form.output,
                    }),
                });
    
                const data = await response.json();
                setResult(data.prompt);
                setAccuracy(data.score);
            } catch (err) {
                console.log(err);
            } finally {
                setGeneratingprompt(false);
            }
        } else {
            alert("Please provide a proper prompt");
        }
    };
    
    


    const handleSubmit = async (e) => {
        e.preventDefault();
    
        if (form.scenario && form.preview) {
            setLoading(true);
            try {
                const response = await fetch(
                    "http://192.168.137.236:8000/generate",
                    {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify({ ...form}),
                    }
                );
    
                if (response.ok) {
                    const responseData = await response.json();
                    // Assuming the response has a property named "result"
                    const result = responseData.result;
    
                    // Do something with the result
                    console.log(result);
                    // You can also update your UI or state with the received result
                } else {
                    console.log("Failed to get a successful response from the server");
                }
            } catch (err) {
                console.error(err);
            } finally {
                setLoading(false);
            }
        } else {
            alert("Please generate a prompt with proper details");
        }
    };
    
    return (
        <section className="bg-hero min-h-[calc(100vh)]">
            <div className="max-w-7xl bg-hero sm:p-8 px-4 mt-16 m-auto">
                <div>
                    <h1 className="font-extrabold text-text text-[42px]">Insert your preferences</h1>
                </div>

                <form className="mt-2 form" onSubmit={handleSubmit}>
                    <div className="flex my-auto flex-col gap-5">
                        <FormFields
                            labelName="The objective"
                            type="text"
                            name="objective"
                            placeholder="Enter Your Objective"
                            value={form.objective}
                            handleChange={handleChange}
                        />
                        <FormFields
                            labelName="The output"
                            type="text"
                            name="output"
                            placeholder="Enter the desired output"
                            value={form.output}
                            handleChange={handleChange}
                        />
                        <FormFields
                            labelName="Scenario"
                            type="text"
                            name="scenario"
                            placeholder="Enter a prompt..."
                            value={form.scenario}
                            handleChange={handleChange}
                            isSurpriseMe
                            handleSurpriseMe={handleSurpriseMe}
                        />

                        <div className="mt-2 flex flex-col">
                            <button
                                type="button"
                                onClick={generatePrompt}
                                className="text-black bg-accent font-bold rounded-md text-sm w-full sm:w-auto px-5 py-2.5 text-center"
                            >
                                {generatingprompt ? "Generating..." : "Generate Prompt"}
                            </button>
                            <button
                                type="submit"
                                className="mt-3 text-white bg-brand text-black font-bold rounded-md text-sm sm:w-auto px-5 py-2.5 text-center w-full"
                            >
                                {loading ? "Sharing..." : "Use this directly on chatbot"}
                            </button>
                        </div>
                    </div>
                    <div className="relative form_photo md:m-auto border bg-darkgrey border-darkgrey text-whtie text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 w-64 p-3 h-64 flex flex-col items-center justify-center">
                        {form.preview ? (
                            <span className="text-white mb-2">
                                {result ? result : (form.results || "Generated prompt will be shown here")}
                            </span>
                        ) : (
                            <div className="text-white text-center">
                                <p className="mb-2">{result ? result : (form.results || "Generated prompt will be shown here")}</p>
                                {accuracy && <p className="text-white mt-2">Score: {accuracy}</p>}
                            </div>
                        )}
                    </div>
                </form>
            </div>
        </section>
    );
};

export default CreatePost;
