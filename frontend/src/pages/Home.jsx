import React, { useState, useEffect } from "react";
import { Loader, FormFields, Card } from "../components";
import { preview } from "../assets";
import Pagination from "../components/Pagination";
import { Link } from "react-router-dom";
import { hero } from "../assets/index"

const RenderCards = ({ data, title }) => {
    if (data?.length > 0) {
        return data.map((post) => <Card key={post._id} {...post} />);
    } else {
        return <h2 className="text-brand font-bold text-xl">{title}</h2>;
    }
};

const Home = () => {
    const [loading, setLoading] = useState(false);
    const [allPosts, setAllPosts] = useState([]);
    const [searchText, setSearchText] = useState("");
    const [filteredPosts, setFilteredPosts] = useState([]);
    const [searchTimeout, setSearchTimeout] = useState(null);

    useEffect(() => {
        const fetchPosts = async () => {
            setLoading(true);
            try {
                const response = await fetch(
                    "https://dalle-hn3a.onrender.com/api/v1/post",
                    {
                        method: "GET",
                        headers: {
                            "Content-Type": "application/json",
                        },
                    }
                );

                if (response.ok) {
                    const result = await response.json();
                    setAllPosts(result.data.reverse());
                }
            } catch (err) {
                console.log(err);
            } finally {
                setLoading(false);
            }
        };
        fetchPosts();
    }, []);

    const handleSearchChange = async (e) => {
        clearTimeout(searchTimeout);
        setSearchText(e.target.value);

        setSearchTimeout(
            setTimeout(() => {
                const filteredPosts = allPosts.filter((post) =>
                    post.prompt.toLowerCase().includes(searchText.toLowerCase())
                );
                setFilteredPosts(filteredPosts);
                setLoading(false);
            }, 500)
        );
    };

    // set dynamic imgPerPage value according to screen size
    if (window.innerWidth <= 768) {
        var dynamicPerPage = 3;
    } else {
        dynamicPerPage = 6;
    }

    // implement pagination
    const [currentPage, setCurrentPage] = useState(1);
    const [postsPerPage] = useState(dynamicPerPage);
    const indexOfLastPost = currentPage * postsPerPage;
    const indexOfFirstRepo = indexOfLastPost - postsPerPage;
    const currentPosts = allPosts.slice(indexOfFirstRepo, indexOfLastPost);

    const paginate = (pageNumber) => {
        setCurrentPage(pageNumber);
        window.scrollTo({ top: 0, behavior: "smooth" });
    };

    // calculate page numbers
    const pageNumbers = [];
    for (let i = 1; i <= Math.ceil(allPosts.length / postsPerPage); i++) {
        pageNumbers.push(i);
    }

    return (
        <section className="mx-auto">
            <div className="max-w-7xl sm:p-8 px-4 py-8 m-auto hero">
                <div className="hero__text"> <br />
                    <h1 className="text-text">Prompt Generator</h1>
                    <p className="mt-2 text-text max-w-[520px]">
                        This webpage serves as a prompt generator for the week-6 challenge document.
                    </p>

                    <p className="mt-2 text-text max-w-[500px]">
                    Specify the objective, scenario, and your desired output so that we can generate prompts for the chatbot.
                    </p>
                    <br />
                    <Link
                        to="/create"
                        className="font-inter  font-bold bg-accent text-black px-2 py-1 rounded-md"
                    >
                        Create Prompt
                    </Link>
                </div>
                <div className="hero__img">
                    <img src={hero} alt="img" />
                </div>
            </div>
        </section>
    );
};

export default Home;
