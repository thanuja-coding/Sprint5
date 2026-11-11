import { useState, useEffect } from "react";
import { useParams ,Link } from "react-router"

function ProductDetailPage() {
    const {id} =useParams();
    const[product,setProducts] =useState(null);

    useEffect(() => {
        async function loadProducts(){
        
            const res = await fetch(`https://dummyjson.com/products/${id}`);
            const data = await res.json();

            setProducts(data);
        }
        loadProducts();
    },[id]);
    if (!product) return <p>Loading.....</p>;

   return (
    <>
    <Link to="/">Back to products</Link>
    <h2>{product.title}</h2>
    <p>Description:{product.description}</p>
    <p>Price: ${product.price}</p>
    <p>Rating:{product.rating}</p>
    <p>Category:{product.category}</p>
    <p>Stock:{product.stock}</p>
    <h3>images:</h3>
    <ul>
        {product.reviews.map((reviews)=> (
            <li key ={reviews.reviewerEmail}>
                {reviews.reviewerName}({reviews.rating}/5): {reviews.comment}
            </li>
        ))}
    </ul>


    </>
   )
}
export default ProductDetailPage