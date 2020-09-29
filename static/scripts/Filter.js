import React from 'react';
import '../shop.css';
import {isMobile} from 'react-device-detect';

export const Filter = ({ brands, loading, changeFilter, submitForm, close }) => {
    // let brand_list = [];
    // if (loading == true) {
    //     brand_list = <div>Loading...</div>
    // }
    // else {
    //     brand_list = brands.map((x, i) => {
    //         <div key={x} className="custom-control custom-radio">
    //             <input type="radio" value={x} id={ "brandRadio" + i.toString()} name="brand" className="custom-control-input"></input>
    //             <label className="custom-control-label" for={ "brandRadio" + i.toString()}>{ x }</label>
    //         </div>
    //     })
    // }
    if (isMobile) {
        return (
            <div id="myNavo" class="overlay-o">
            <a href="javascript:void(0)" class="closebtn-o" onClick={close}>&times;</a>
                <div class="overlay-content-o">
                {loading ? (<h5 className="text-center">Loading...</h5>) : (<div>
                    {[1].map(x => {
    
                        const brand_list = brands.map((x, i) => {
                            return (<div key={x} className="custom-control custom-radio">
                                <input key={x + 'x'+ i} type="radio" onClick={e => changeFilter( 2, x)} value={x} id={ "brandRadio" + i.toString()} name="brand" className="custom-control-input"></input>
                                <label key={x + i} className="custom-control-label" htmlFor={ "brandRadio" + i.toString()}>{ x }</label>
                                </div>)
                        })
    
                        return (
                            <form key="1" onSubmit={submitForm}>
                                <div className="accordion" id="accordionExample">
                                    <div className="card" type="button" data-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
                                        <div className="card-header" id="headingOne">
                                            <p className="mb-0">
                                            <span className="btn btn-link w-100" type="button" data-toggle="collapse" data-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
                                                <svg width="1em" height="1em" viewBox="0 0 16 16" className="bi bi-person-square mb-1 mr-1" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                                                    <path fillRule="evenodd" d="M14 1H2a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z"/>
                                                    <path fillRule="evenodd" d="M2 15v-1c0-1 1-4 6-4s6 3 6 4v1H2zm6-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/>
                                                    </svg> Gender
                                            </span>
                                        </p>
                                        </div>
                                        <div id="collapseOne" className="collapse" aria-labelledby="headingOne">
                                            <div className="card-body">
                                                <div className="custom-control custom-radio">
                                                    <input type="radio" onClick={e => changeFilter( 0, "Men's watch/Unisex")} value="Men's watch/Unisex" id="radioButtonID" name="gender" className="custom-control-input"></input>
                                                    <label className="custom-control-label" htmlFor="radioButtonID">Men's/Unisex</label>
                                                </div>
                                                <div className="custom-control custom-radio">
                                                    <input type="radio" onClick={e => changeFilter( 0, "Women's")} value="Women's" id="genderRadio2" name="gender" className="custom-control-input"></input>
                                                    <label className="custom-control-label" htmlFor="genderRadio2">Women's</label>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div className="card" type="button" data-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
                                        <div className="card-header" id="headingTwo">
                                            <h2 className="mb-0">
                                            <span className="btn btn-link collapsed w-100" type="button" data-toggle="collapse" data-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
                                                <svg width="1em" height="1em" viewBox="0 0 16 16" className="bi bi-tags-fill mb-1 mr-1" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                                                    <path fillRule="evenodd" d="M3 1a1 1 0 0 0-1 1v4.586a1 1 0 0 0 .293.707l7 7a1 1 0 0 0 1.414 0l4.586-4.586a1 1 0 0 0 0-1.414l-7-7A1 1 0 0 0 7.586 1H3zm4 3.5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0z"/>
                                                    <path d="M1 7.086a1 1 0 0 0 .293.707L8.75 15.25l-.043.043a1 1 0 0 1-1.414 0l-7-7A1 1 0 0 1 0 7.586V3a1 1 0 0 1 1-1v5.086z"/>
                                                </svg> Category
                                            </span>
                                            </h2>
                                        </div>
                                        <div id="collapseTwo" className="collapse" aria-labelledby="headingTwo">
                                            <div className="card-body">
                                                <div className="custom-control custom-radio">
                                                    <input type="radio" onClick={e => changeFilter(1, "Smartwatch")} value="Smartwatch" id="categoryRadio1" name="category" className="custom-control-input"></input>
                                                    <label className="custom-control-label" htmlFor="categoryRadio1">Smartwatch</label>
                                                </div>
                                                <div className="custom-control custom-radio">
                                                    <input type="radio" onClick={e => changeFilter(1, "Chronograph")} value="Chronograph" id="categoryRadio2" name="category" className="custom-control-input"></input>
                                                    <label className="custom-control-label" htmlFor="categoryRadio2">Chronograph</label>
                                                </div>
                                                <div className="custom-control custom-radio">
                                                    <input type="radio" onClick={e => changeFilter(1, "GMT watch")} value="GMT watch" id="categoryRadio3" name="category" className="custom-control-input"></input>
                                                    <label className="custom-control-label" htmlFor="categoryRadio3">GMT watch</label>
                                                </div>
                                                <div className="custom-control custom-radio">
                                                    <input type="radio" onClick={e => changeFilter(1, "Diver's watch")} value="Diver's watch" id="categoryRadio4" name="category" className="custom-control-input"></input>
                                                    <label className="custom-control-label" htmlFor="categoryRadio4">Diver's watch</label>
                                                </div>
                                                <div className="custom-control custom-radio">
                                                    <input type="radio" onClick={e => changeFilter(1, "Pilot watch")} value="Pilot watch" id="categoryRadio5" name="category" className="custom-control-input"></input>
                                                    <label className="custom-control-label" htmlFor="categoryRadio5">Pilot watch</label>
                                                </div>
                                                <div className="custom-control custom-radio">
                                                    <input type="radio" onClick={e => changeFilter(1, "Casual")} value="Casual" id="categoryRadio6" name="category" className="custom-control-input"></input>
                                                    <label className="custom-control-label" htmlFor="categoryRadio6">Casual</label>
                                                </div>
                                                <div className="custom-control custom-radio">
                                                    <input type="radio" onClick={e => changeFilter(1, "Dress watch")} value="Dress watch" id="categoryRadio7" name="category" className="custom-control-input"></input>
                                                    <label className="custom-control-label" htmlFor="categoryRadio7">Dress watch</label>
                                                </div>
                                                <div className="custom-control custom-radio">
                                                    <input type="radio" onClick={e => changeFilter(1, "Other")} value="Other" id="categoryRadio8" name="category" className="custom-control-input"></input>
                                                    <label className="custom-control-label" htmlFor="categoryRadio8">Other</label>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div className="card" type="button" data-target="#collapseThree" aria-expanded="false" aria-controls="collapseThree">
                                        <div className="card-header" id="headingThree">
                                            <h2 className="mb-0">
                                            <span className="btn btn-link collapsed w-100" type="button" data-toggle="collapse" data-target="#collapseThree" aria-expanded="false" aria-controls="collapseThree">
                                                <svg width="1em" height="1em" viewBox="0 0 16 16" className="bi bi-patch-check-fll mb-1 mr-1" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                                                    <path fillRule="evenodd" d="M10.067.87a2.89 2.89 0 0 0-4.134 0l-.622.638-.89-.011a2.89 2.89 0 0 0-2.924 2.924l.01.89-.636.622a2.89 2.89 0 0 0 0 4.134l.637.622-.011.89a2.89 2.89 0 0 0 2.924 2.924l.89-.01.622.636a2.89 2.89 0 0 0 4.134 0l.622-.637.89.011a2.89 2.89 0 0 0 2.924-2.924l-.01-.89.636-.622a2.89 2.89 0 0 0 0-4.134l-.637-.622.011-.89a2.89 2.89 0 0 0-2.924-2.924l-.89.01-.622-.636zm.287 5.984a.5.5 0 0 0-.708-.708L7 8.793 5.854 7.646a.5.5 0 1 0-.708.708l1.5 1.5a.5.5 0 0 0 .708 0l3-3z"/>
                                                    </svg> Brands
                                            </span>
                                            </h2>
                                        </div>
                                        <div id="collapseThree" className="collapse" aria-labelledby="headingThree">
                                            <div className="card-body">
                                                { brand_list }                                     
                                            </div>
                                        </div>
                                    </div>                
                                </div>
                                <button type="submit" className="btn btn-secondary float-right m-2">
                                    <svg width="1em" height="1em" viewBox="0 0 16 16" className="bi bi-filter" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                                        <path fillRule="evenodd" d="M6 10.5a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5zm-2-3a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7a.5.5 0 0 1-.5-.5zm-2-3a.5.5 0 0 1 .5-.5h11a.5.5 0 0 1 0 1h-11a.5.5 0 0 1-.5-.5z"/>
                                    </svg> Filter
                                </button>
                            </form>
                        )
                    })
                }</div>)}
            </div>
        </div>
        )
    }
    return (
        <div>
            {loading ? (<h5 className="text-center">Loading...</h5>) : (<div>
                {[1].map(x => {

                    const brand_list = brands.map((x, i) => {
                        return (<div key={x} className="custom-control custom-radio">
                            <input key={x + 'x'+ i} type="radio" onClick={e => changeFilter( 2, x)} value={x} id={ "brandRadio" + i.toString()} name="brand" className="custom-control-input"></input>
                            <label key={x + i} className="custom-control-label" htmlFor={ "brandRadio" + i.toString()}>{ x }</label>
                            </div>)
                    })

                    return (
                        <form className="mt-4" key="1" onSubmit={submitForm}>
                            <div className="accordion" id="accordionExample">
                                <div className="card" type="button" data-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
                                    <div className="card-header" id="headingOne">
                                        <p className="mb-0">
                                        <span className="btn btn-link w-100" type="button" data-toggle="collapse" data-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
                                            <svg width="1em" height="1em" viewBox="0 0 16 16" className="bi bi-person-square mb-1 mr-1" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                                                <path fillRule="evenodd" d="M14 1H2a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z"/>
                                                <path fillRule="evenodd" d="M2 15v-1c0-1 1-4 6-4s6 3 6 4v1H2zm6-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/>
                                                </svg> Gender
                                        </span>
                                    </p>
                                    </div>
                                    <div id="collapseOne" className="collapse" aria-labelledby="headingOne">
                                        <div className="card-body">
                                            <div className="custom-control custom-radio">
                                                <input type="radio" onClick={e => changeFilter( 0, "Men's watch/Unisex")} value="Men's watch/Unisex" id="genderRadio1" name="gender" className="custom-control-input"></input>
                                                <label className="custom-control-label" htmlFor="genderRadio1">Men's/Unisex</label>
                                            </div>
                                            <div className="custom-control custom-radio">
                                                <input type="radio" onClick={e => changeFilter( 0, "Women's")} value="Women's" id="genderRadio2" name="gender" className="custom-control-input"></input>
                                                <label className="custom-control-label" htmlFor="genderRadio2">Women's</label>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div className="card" type="button" data-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
                                    <div className="card-header" id="headingTwo">
                                        <h2 className="mb-0">
                                        <span className="btn btn-link collapsed w-100" type="button" data-toggle="collapse" data-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
                                            <svg width="1em" height="1em" viewBox="0 0 16 16" className="bi bi-tags-fill mb-1 mr-1" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                                                <path fillRule="evenodd" d="M3 1a1 1 0 0 0-1 1v4.586a1 1 0 0 0 .293.707l7 7a1 1 0 0 0 1.414 0l4.586-4.586a1 1 0 0 0 0-1.414l-7-7A1 1 0 0 0 7.586 1H3zm4 3.5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0z"/>
                                                <path d="M1 7.086a1 1 0 0 0 .293.707L8.75 15.25l-.043.043a1 1 0 0 1-1.414 0l-7-7A1 1 0 0 1 0 7.586V3a1 1 0 0 1 1-1v5.086z"/>
                                            </svg> Category
                                        </span>
                                        </h2>
                                    </div>
                                    <div id="collapseTwo" className="collapse" aria-labelledby="headingTwo">
                                        <div className="card-body">
                                            <div className="custom-control custom-radio">
                                                <input type="radio" onClick={e => changeFilter(1, "Smartwatch")} value="Smartwatch" id="categoryRadio1" name="category" className="custom-control-input"></input>
                                                <label className="custom-control-label" htmlFor="categoryRadio1">Smartwatch</label>
                                            </div>
                                            <div className="custom-control custom-radio">
                                                <input type="radio" onClick={e => changeFilter(1, "Chronograph")} value="Chronograph" id="categoryRadio2" name="category" className="custom-control-input"></input>
                                                <label className="custom-control-label" htmlFor="categoryRadio2">Chronograph</label>
                                            </div>
                                            <div className="custom-control custom-radio">
                                                <input type="radio" onClick={e => changeFilter(1, "GMT watch")} value="GMT watch" id="categoryRadio3" name="category" className="custom-control-input"></input>
                                                <label className="custom-control-label" htmlFor="categoryRadio3">GMT watch</label>
                                            </div>
                                            <div className="custom-control custom-radio">
                                                <input type="radio" onClick={e => changeFilter(1, "Diver's watch")} value="Diver's watch" id="categoryRadio4" name="category" className="custom-control-input"></input>
                                                <label className="custom-control-label" htmlFor="categoryRadio4">Diver's watch</label>
                                            </div>
                                            <div className="custom-control custom-radio">
                                                <input type="radio" onClick={e => changeFilter(1, "Pilot watch")} value="Pilot watch" id="categoryRadio5" name="category" className="custom-control-input"></input>
                                                <label className="custom-control-label" htmlFor="categoryRadio5">Pilot watch</label>
                                            </div>
                                            <div className="custom-control custom-radio">
                                                <input type="radio" onClick={e => changeFilter(1, "Casual")} value="Casual" id="categoryRadio6" name="category" className="custom-control-input"></input>
                                                <label className="custom-control-label" htmlFor="categoryRadio6">Casual</label>
                                            </div>
                                            <div className="custom-control custom-radio">
                                                <input type="radio" onClick={e => changeFilter(1, "Dress watch")} value="Dress watch" id="categoryRadio7" name="category" className="custom-control-input"></input>
                                                <label className="custom-control-label" htmlFor="categoryRadio7">Dress watch</label>
                                            </div>
                                            <div className="custom-control custom-radio">
                                                <input type="radio" onClick={e => changeFilter(1, "Other")} value="Other" id="categoryRadio8" name="category" className="custom-control-input"></input>
                                                <label className="custom-control-label" htmlFor="categoryRadio8">Other</label>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div className="card" type="button" data-target="#collapseThree" aria-expanded="false" aria-controls="collapseThree">
                                    <div className="card-header" id="headingThree">
                                        <h2 className="mb-0">
                                        <span className="btn btn-link collapsed w-100" type="button" data-toggle="collapse" data-target="#collapseThree" aria-expanded="false" aria-controls="collapseThree">
                                            <svg width="1em" height="1em" viewBox="0 0 16 16" className="bi bi-patch-check-fll mb-1 mr-1" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                                                <path fillRule="evenodd" d="M10.067.87a2.89 2.89 0 0 0-4.134 0l-.622.638-.89-.011a2.89 2.89 0 0 0-2.924 2.924l.01.89-.636.622a2.89 2.89 0 0 0 0 4.134l.637.622-.011.89a2.89 2.89 0 0 0 2.924 2.924l.89-.01.622.636a2.89 2.89 0 0 0 4.134 0l.622-.637.89.011a2.89 2.89 0 0 0 2.924-2.924l-.01-.89.636-.622a2.89 2.89 0 0 0 0-4.134l-.637-.622.011-.89a2.89 2.89 0 0 0-2.924-2.924l-.89.01-.622-.636zm.287 5.984a.5.5 0 0 0-.708-.708L7 8.793 5.854 7.646a.5.5 0 1 0-.708.708l1.5 1.5a.5.5 0 0 0 .708 0l3-3z"/>
                                                </svg> Brands
                                        </span>
                                        </h2>
                                    </div>
                                    <div id="collapseThree" className="collapse" aria-labelledby="headingThree">
                                        <div className="card-body">
                                            { brand_list }                                     
                                        </div>
                                    </div>
                                </div>                
                            </div>
                            <button type="submit" className="btn btn-secondary float-right m-2">
                                <svg width="1em" height="1em" viewBox="0 0 16 16" className="bi bi-filter" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                                    <path fillRule="evenodd" d="M6 10.5a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5zm-2-3a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7a.5.5 0 0 1-.5-.5zm-2-3a.5.5 0 0 1 .5-.5h11a.5.5 0 0 1 0 1h-11a.5.5 0 0 1-.5-.5z"/>
                                </svg> Filter
                            </button>
                        </form>
                    )
                })
            }</div>)}
        </div>
    )};