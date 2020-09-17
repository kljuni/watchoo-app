import React, { useEffect, useState } from 'react';
import { Watches } from './Watches';
import { Form, Button, Container, Row, Col } from 'react-bootstrap';
import { Pages } from './Pagination';
import { Filter } from './Filter';

function App() {
    const [watches, setWatches] = useState([]);
    const [images, setImages] = useState([]);
    const [order, setOrder] = useState(1);
    const [num_pages, setNum_pages] = useState(0);
    const [cur_page, setCur_page] = useState(1);
    const [loading, setLoading] = useState(true);
    const [showMore, setShowMore] = useState(true);
    const [brands, setBrands] = useState([]);
    const [gender, setGender] = useState("");
    const [category, setCategory] = useState("");
    const [brand, setBrand] = useState("");
    const [submit, setSubmit] = useState(0);


    useEffect(() => {
        // console.log('/api/shop/' + order + '/' + cur_page + '?arg1=' + gender + '&arg2=' + category + '&arg3=' + brand)
        fetch('/api/shop/' + order + '/' + cur_page + '?arg1=' + encodeURIComponent(gender) + '&arg2=' + encodeURIComponent(category) + '&arg3=' + encodeURIComponent(brand))
        .then(response => response.json()
        .then(data => {
            setWatches(data.watches);
            setImages(data.images);
            setNum_pages(data.num_pages);
            setLoading(false);
            setBrands(data.brands);
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
        window.scrollTo(0, 0);
    }

    const Sorting = () => {
        return (
        <div className="mt-4">
            {showMore ? null : (
                <Form.Group>
                    <Form.Row>
                        <Col>
                        <a className="text-secondary ml-1" href="mailto:ivan.kljun@navix.si"><i>Advertise at Watcho.com</i></a>
                        </Col>
                        <Col xs="auto" className="ml-auto ml-md-0 mr-1 my-0">
                            <Form.Control size="sm" as="select" onChange={e => changeOrder(e.target.value)}>
                                <option value="1" >Newest ads first</option>
                                <option value="2" >Oldest ads first</option>
                                <option value="3" >Price ascending</option>
                                <option value="4" >Price descending</option>
                            </Form.Control>
                        </Col>
                    </Form.Row>
                </Form.Group>
            )}
        </div>
        )
    } 

    const More = () => {
        const onClick = () => {
            setShowMore(false);
            Sorting();
            window.scrollTo(0, 0);
        }
        return (
          <div className="d-flex justify-content-center">
            { showMore ? <Button className="text-center my-5" variant="secondary" onClick={onClick}>Show more »</Button> : 
            <Pages changePage={changePage} cur_page={cur_page} loading={loading} num_pages={num_pages}/> }
          </div>
        )
      }

    const changeFilter = (x,y) => {
        if (x == 0) {
            console.log(y);
            if (gender == y) {
                setGender('');
                document.getElementById("radioButtonID").checked = false;
            }
            setGender(y);
            console.log(gender + " is now")
        }
        else if (x == 1) {
            console.log(y);
            setCategory(y);
        }
        else if (x == 2) {
            console.log(y);
            setBrand(y);
        }
    }

    const close = () => {
        document.getElementById("myNavo").style.display = "none"
    }

    const open = () => {
        document.getElementById("myNavo").style.display = "block"
    }

    const submitForm = (event) => {
        event.preventDefault()
        fetch('/api/shop/' + order + '/' + cur_page + '?arg1=' + gender + '&arg2=' + category + '&arg3=' + brand)
        .then(response => response.json()
        .then(data => {
            setWatches(data.watches);
            setImages(data.images);
            // setNum_pages(data.num_pages);
            // setLoading(false);
            // setBrands(data.brands);
        }))
        document.getElementById("myNavo").style.display = "none";
    }

    return (
        <Container>
            <Row>
                <Col xs={0} md={2}>
                </Col>
                <Col xs={12} md={7}>
                    <Sorting />
                    <Watches watches={watches} images={images} loading={loading} open={open} />
                    <More />
                </Col>
                <Col xs={12} md={3}>
                    <Filter brands={brands} loading={loading} changeFilter={changeFilter} useEffect={useEffect} submitForm={submitForm} close={close} />
                </Col>
            </Row>
        </Container>
    );
}

export default App;