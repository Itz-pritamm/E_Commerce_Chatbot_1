from semantic_router import Route
from semantic_router.routers import SemanticRouter
from semantic_router.encoders import HuggingFaceEncoder


encoder=HuggingFaceEncoder(
    name="sentence-transformers/all-MiniLM-L6-v2"
)


faq = Route(
    name="faq",
    utterances=[
        # Return / Refund
        "What is the return policy?",
        "How can I return a product?",
        "How do I return my order?",
        "What if I want to return an item?",
        "Refund policy details",
        "How long does refund take?",
        "When will I get my refund?",
        
        # Order Tracking
        "How can I track my order?",
        "Track my order",
        "Where is my order?",
        "Check order status",
        "Order tracking",
        
        # Payments
        "What payment methods are accepted?",
        "Payment options available",
        "Can I pay using credit card?",
        "Do you accept debit card?",
        "did you accept the cash payment",
        
        # Offers / Discounts
        "Do I get discount with HDFC credit card?",
        "Any bank offers available?",
        "Are there any discounts on payment?"
    ]
)

sql = Route(
    name="sql",
    utterances=[
        "I want to buy nike shoes with discount",
        "Nike shoes 50% off",
        "Show me cheap Nike shoes",
        "Are there any shoes under Rs 3000?",
        "Budget shoes under 3k",
        "Low price shoes",
        "Do you have formal shoes in size 9?",
        "Shoes size 9 available?",
        "Men shoes size 9",
        "Are there any Puma shoes on sale?",
        "Discount on Puma shoes",
        "Puma shoes offers",
        "What is the price of puma running shoes?",
        "Price of running shoes",
        "Show running shoes price"
        "give me top 3 shoes in descending order of rating",
    ]
)
router = SemanticRouter(
    routes=[faq, sql],
    encoder=encoder,
    auto_sync="local"
     
)

if __name__=="__main__":
    print(router("How can I track my order?").name)
    print(router("show me the puma shoes in red color price range is 5k to 6 k?").name)
