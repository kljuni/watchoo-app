import React from 'react';
import { Card } from 'react-bootstrap';


export const Watches = ({ watches, images, loading }) => {
    return (
        <div>
            {loading ? (<h1>Loading...</h1>) : (<div>
                {watches.map(watch => {                
                    let counter = 0;
                    const img_list = images.map(image => {
                        if ((watch[0] == image[0]) && (counter == 0)) {
                            counter++
                            return <img key={image[3]} src={image[3]} className="img-fluid display-pic" alt="Responsive image"/>
                        }
                    })
                    return(
                        <a key={ watch[0] } href={ "/watch/" + watch[0] } className="list-group-item list-group-item-action align-items-start h-oglas mt-2">
                            <div className="row">
                                <div className="col-3 text-center my-auto">        
                                {img_list}  
                                </div>
                                <div className="col-9">
                                    <Card>
                                    <Card.Body>
                                    <Card.Title>{ watch[1] } - { watch[2] }</Card.Title>
                                        <hr className="my-2"></hr>
                                        <p className="small">
                                            <svg width="1em" height="1em" viewBox="0 0 16 16" className="bi bi-tags-fill mb-1 mr-1" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                                                <path fillRule="evenodd" d="M3 1a1 1 0 0 0-1 1v4.586a1 1 0 0 0 .293.707l7 7a1 1 0 0 0 1.414 0l4.586-4.586a1 1 0 0 0 0-1.414l-7-7A1 1 0 0 0 7.586 1H3zm4 3.5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0z"/>
                                                <path d="M1 7.086a1 1 0 0 0 .293.707L8.75 15.25l-.043.043a1 1 0 0 1-1.414 0l-7-7A1 1 0 0 1 0 7.586V3a1 1 0 0 1 1-1v5.086z"/>
                                            </svg> Hand watches
                                            <svg width="1em" height="1em" viewBox="0 0 16 16" className="bi bi-geo-alt mb-1 mr-1 ml-3" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                                                <path fillRule="evenodd" d="M8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10zm0-7a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/>
                                            </svg> Ljubljana
                                            <svg width="1em" height="1em" viewBox="0 0 16 16" className="bi bi-person mb-1 mr-1 ml-3" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                                                <path fillRule="evenodd" d="M13 14s1 0 1-1-1-4-6-4-6 3-6 4 1 1 1 1h10zm-9.995-.944v-.002.002zM3.022 13h9.956a.274.274 0 0 0 .014-.002l.008-.002c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.289 10 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664a1.05 1.05 0 0 0 .022.004zm9.974.056v-.002.002zM8 7a2 2 0 1 0 0-4 2 2 0 0 0 0 4zm3-2a3 3 0 1 1-6 0 3 3 0 0 1 6 0z"/>
                                            </svg> Private seller                          
                                        </p>
                                        <div className="d-flex small mt-4">
                                            <div>
                                                <p className="mb-0">Movement:</p>
                                                <p className="mb-0">Year of production:</p>
                                                <p className="mb-0">Condition:</p>
                                            </div>
                                            <div className="ml-4">
                                                <b><p className="mb-0">{ watch[6] }</p></b>
                                                <b><p className="mb-0">{ watch[5] }</p></b>
                                                <b><p className="mb-0">{ watch[3] }</p></b>
                                            </div>
                                            <div className="ml-auto mt-auto text-nowrap">
                                                <h4 className="mb-0">{ watch[7] } €</h4>
                                            </div>
                                        </div>
                                    </Card.Body>
                                    </Card>
                                </div>
                            </div>
                        </a>                    
                    )
                })}
                </div>
            )}
        </div>
    )
}

// '{/* <a href="#" className="list-group-item list-group-item-action align-items-start h-oglas mt-2">
//                         <div className="row">
//                         <Button>Test button</Button>
//                             <div className="col-3 text-center my-auto">
//                                 {images.map((image, i) => {
//                                     if (watch[0] == image[0]) {
//                                         return <img src={images[i][3]} className="img-fluid display-pic" alt="Responsive image"/>
//                                     }
//                                 })}                                         
//                             </div>
//                         </div>
//                     </a>

// <a href="{{ url_for('watch', item_id = row[0]) }}" class="list-group-item list-group-item-action align-items-start h-oglas mt-2">
//                 <div class="row">
//                     <div class="col-3 text-center my-auto">
                        
//                         {% for image in images if image[0] == row[0] %}
//                             {% if loop.index <= 1 %}
//                             <img src="{{ image[3] }}" class="img-fluid display-pic" alt="Responsive image">
//                             {% endif %}
//                         {% endfor %}
                                            
//                     </div>
//                     <div class="col-9">
//                         <h6 class="card-title">{{ row[1] }} - {{ row[2] }}</h6>
//                         <hr class="my-2">
//                         <p class="small">
//                             <svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-tags-fill mb-1 mr-1" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
//                                 <path fill-rule="evenodd" d="M3 1a1 1 0 0 0-1 1v4.586a1 1 0 0 0 .293.707l7 7a1 1 0 0 0 1.414 0l4.586-4.586a1 1 0 0 0 0-1.414l-7-7A1 1 0 0 0 7.586 1H3zm4 3.5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0z"/>
//                                 <path d="M1 7.086a1 1 0 0 0 .293.707L8.75 15.25l-.043.043a1 1 0 0 1-1.414 0l-7-7A1 1 0 0 1 0 7.586V3a1 1 0 0 1 1-1v5.086z"/>
//                             </svg> Hand watches
//                             <svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-geo-alt mb-1 mr-1 ml-3" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
//                                 <path fill-rule="evenodd" d="M8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10zm0-7a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/>
//                             </svg> Ljubljana
//                             <svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-person mb-1 mr-1 ml-3" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
//                                 <path fill-rule="evenodd" d="M13 14s1 0 1-1-1-4-6-4-6 3-6 4 1 1 1 1h10zm-9.995-.944v-.002.002zM3.022 13h9.956a.274.274 0 0 0 .014-.002l.008-.002c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.289 10 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664a1.05 1.05 0 0 0 .022.004zm9.974.056v-.002.002zM8 7a2 2 0 1 0 0-4 2 2 0 0 0 0 4zm3-2a3 3 0 1 1-6 0 3 3 0 0 1 6 0z"/>
//                             </svg> Private seller                          
//                         </p>
//                         <div class="d-flex small mt-4">
//                             <div>
//                                 <p class="mb-0">Movement:</p>
//                                 <p class="mb-0">Year of production:</p>
//                                 <p class="mb-0">Condition:</p>
//                             </div>
//                             <div class="ml-4">
//                                 <b><p class="mb-0">{{ row[6] }}</p></b>
//                                 <b><p class="mb-0">{{ row[5] }}</p></b>
//                                 <b><p class="mb-0">{{ row[3] }}</p></b>
//                             </div>
//                             <div class="ml-auto mt-auto text-nowrap">
//                                 <h4 class="mb-0">{{ row[7] }} €</h4>
//                             </div>
//                         </div>
//                     </div>
//                 </div>
//             </a> */}'