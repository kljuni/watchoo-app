import React from 'react';
 
export const Pages = ({ changePage, num_pages, loading, cur_page }) => {
    let l1= null;
    let l2 = null;
    if (!loading) {
        if (cur_page > 1) {
            l1 = <li value="-1" className="page-item"><a className="page-link" onClick={e => changePage(-1)}>«</a></li>
            } else l1 = null;
        if (cur_page < num_pages.length) {
            l2 = <li value="-2" className="page-item"><a className="page-link" onClick={e => changePage(-2)}>»</a></li>
        } else l2 = null;
    }
    return (
        <div>
            {loading ? (<h3>Loading pagination...</h3>) : (
            <div>
                <nav aria-label="Page navigation example">
                    <ul className="pagination my-5">
                        {l1}
                        {num_pages.map((page, i) => {
                            if (page == cur_page) page = <b>{page}</b>;
                            return <li key={i} value={page} className="page-item"><a className="page-link" onClick={e => changePage(page)}>{page}</a></li>
                        })}
                        {l2}
                    </ul>
                </nav>
            </div>)}
        </div>
    )};

