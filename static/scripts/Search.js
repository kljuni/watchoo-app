import React, { useEffect, useState } from 'react';
import { Form } from 'react-bootstrap';
import '../shop.css';

function Search() {
    const [search, setSearch] = useState("");

    const submitSearch = (event) => {
        event.preventDefault()
        setSearch(event.target.value);
        console.log(event.target.value)
    }
    return (
        <Form.Group>
            <Form.Control onChange={submitSearch} size="lg" type="text" placeholder="Large text" />
        </Form.Group>
    );
}

export default Search;