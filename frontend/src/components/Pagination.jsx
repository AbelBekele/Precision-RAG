import React from 'react';

const Pagination = ({ currentPage, paginate, pageNumbers, allPosts, postsPerPage }) => {
    return (
        <div className="mt-4 flex justify-center">
            {/* pagination with prev and next buttons */}
            <button
                onClick={() => paginate(currentPage - 1)}
                disabled={currentPage === 1}
                className="prev"
            >
                Prev
            </button>

            {pageNumbers.map((number) => (
                <button
                    key={number}
                    onClick={() => paginate(number)}
                    className={number === currentPage ? "paginate active" : "paginate"}
                >
                    {number}
                </button>
            ))}
            <button
                onClick={() => paginate(currentPage + 1)}
                disabled={currentPage === Math.ceil(allPosts.length / postsPerPage)}
                className="next"
            >
                Next
            </button>
        </div>
    )
}

export default Pagination