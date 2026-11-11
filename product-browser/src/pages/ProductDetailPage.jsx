import {useState, useEffect} from 'react'
import { Link, useParams} from 'react-router'

function ProductDetailPage() {
    const {id} = useParams();
    const [product, setProduct] = useState(null);

    useEffect(()=>{
        async function loadProduct(){
            const res = await fetch(`https://dummyjson.com/products/${id}`);
            const data = await res.json();
            setProduct(data);
        }
        loadProduct();
    }, [id]);

    if(!product) return <p>Loading...</p>
    

    return (
        <>
            <Link to="/">Back to Products</Link>
            <h2>{product.title}</h2>
            <img src={product.thumbnail} alt={product.title} />
            <p>{product.description}</p>
            <p>Price: ${product.price}</p>
            <p>Rating: {product.rating}</p>
            <p>Category: {product.category}</p>
            <p>Stock: {product.stock}</p>
            <h2>Images</h2>
            {product.images.map((image) => (
                <img key={image} src={image} width="150" />
            ))}
            <h3>Reviews</h3>
            <ul>
                {product.reviews.map((review, index) => (
                    <li key={index}>
                        <p>{review.reviewerName}</p>
                        <p>Rating: {review.rating}</p>
                        <p>{review.comment}</p>
                    </li>
                ))}
            </ul>
        </>
    )

}

export default ProductDetailPage;
