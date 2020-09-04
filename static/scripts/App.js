import React, { useEffect, useState } from 'react';
import { Watches } from './Watches';
import { Form, Button } from 'react-bootstrap';
import { Pages } from './Pagination';

function App() {
    const [watches, setWatches] = useState([]);
    const [images, setImages] = useState([]);
    const [order, setOrder] = useState(1);
    const [num_pages, setNum_pages] = useState(0);
    const [cur_page, setCur_page] = useState(1);
    const [loading, setLoading] = useState(true);
    const [showMore, setShowMore] = useState(true);

    useEffect(() => {
        fetch('/shop/' + order + '/' + cur_page)
        .then(response => response.json()
        .then(data => {
            setWatches(data.watches);
            setImages(data.images);
            setNum_pages(data.num_pages);
            setLoading(false);
        }))
    }, [order, cur_page]);

    const changeOrder = (val) => {
        setOrder(val);
    }
    const changePage = (val) => {
        if (val == "-1") {
            if ((cur_page - 1) > 0) {
            setCur_page(cur_page - 1)
            }
        }
        else if (val == "-2") setCur_page(cur_page + 1);
        else setCur_page(val);
    }

    const Sorting = () => {
        return (
        <div className="my-3">
            {showMore ? null : (
                <Form.Group>
                    <Form.Control size="sm" as="select" onChange={e => changeOrder(e.target.value)}>
                        <option value="1" >Newest ads first</option>
                        <option value="2" >Oldest ads first</option>
                        <option value="3" >Price ascending</option>
                        <option value="4" >Price descending</option>
                    </Form.Control>
                </Form.Group>
            )}
        </div>
        )
    } 

    const More = () => {
        const onClick = () => {
            setShowMore(false);
            Sorting();
        }
        return (
          <div className="my-4">
            { showMore ? <Button className="text-center" variant="outline-primary" size="lg" onClick={onClick} block>Show more »</Button> : 
            <Pages changePage={changePage} cur_page={cur_page} loading={loading} num_pages={num_pages}/> }
          </div>
        )
      }

    return (
        <div>
            <Sorting />
            <Watches watches={watches} images={images} loading={loading}/>
            <More />
        </div>
    );
}

export default App;