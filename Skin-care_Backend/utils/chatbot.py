"""
Advanced RAG Chatbot with Google Gemini
Combines FAISS vector search + Gemini AI for best results
"""

import json
import numpy as np
import faiss
import os
from sentence_transformers import SentenceTransformer
from config import Config


class SkincareChatbot:
    
    def __init__(self):
        print("\n" + "="*70)
        print("INITIALIZING ADVANCED RAG CHATBOT (GEMINI)")
        print("="*70)
        
        # Load knowledge base
        print("\n Loading skincare knowledge base...")
        with open(Config.KNOWLEDGE_BASE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        self.qa_database = data["qa_database"]
        print(f"    Loaded {len(self.qa_database)} knowledge entries")
        
        # Load embedding model
        print("\n Loading SentenceTransformer...")
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        print("    SentenceTransformer loaded")
        
        # Build FAISS index
        print("\n🔍 Building FAISS index...")
        self._build_faiss_index()
        print(f"    FAISS index built with {self.index.ntotal} vectors")
        
        # Initialize Gemini
        print("\n Initializing Google Gemini...")
        self._init_gemini()
        
        print("\n" + "="*70)
        print(" CHATBOT READY (Gemini + FAISS RAG)")
        print("="*70 + "\n")
    
    def _build_faiss_index(self):
        """Build FAISS index from knowledge base"""
        
        self.documents = []
        
        for item in self.qa_database:
            # Combine question + tags + answer for better matching
            doc_text = f"{item['question']} {' '.join(item['tags'])} {item['answer']}"
            
            self.documents.append({
                "text": doc_text,
                "question": item["question"],
                "answer": item["answer"],
                "tags": item["tags"],
                "id": item["id"],
                "category": item.get("category", "general")
            })
        
        # Generate embeddings
        texts = [doc["text"] for doc in self.documents]
        embeddings = self.embedder.encode(texts, show_progress_bar=True)
        embeddings = np.array(embeddings).astype("float32")
        
        # Normalize for cosine similarity
        faiss.normalize_L2(embeddings)
        
        # Build FAISS index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(embeddings)
    
    def _init_gemini(self):
        """Initialize Google Gemini (new SDK)"""
    
        try:
            from google import genai
            
            api_key = os.getenv("GEMINI_API_KEY")
            
            if not api_key:
                print("    GEMINI_API_KEY not found - using KB fallback")
                self.gemini_client = None
                return
            
            self.gemini_client = genai.Client(api_key=api_key)
            
            print("    Gemini initialized (google-genai)")
    
        except Exception as e:
            print(f"    Gemini initialization failed: {e}")
            print("   ℹ Falling back to direct KB responses")
            self.gemini_client = None
    
    def _retrieve_relevant_docs(self, query, k=3):
        """Retrieve top-k most relevant documents using FAISS"""
        
        # Encode query
        query_embedding = self.embedder.encode([query])
        query_embedding = np.array(query_embedding).astype("float32")
        faiss.normalize_L2(query_embedding)
        
        # Search
        distances, indices = self.index.search(query_embedding, k)
        
        results = []
        for idx, score in zip(indices[0], distances[0]):
            doc = self.documents[idx]
            results.append({
                "question": doc["question"],
                "answer": doc["answer"],
                "score": float(score),
                "tags": doc["tags"],
                "category": doc.get("category", "general")
            })
        
        return results
    
    def _generate_with_gemini(self, query, context_docs, skin_type=None):
        """Generate response using Gemini with retrieved context"""

        if not hasattr(self, "gemini_client") or not self.gemini_client:
                # Fallback to direct answer from best match
            return context_docs[0]["answer"] if context_docs else self._get_fallback(query)
        
        try:
        # 1. Build context from top 3 docs
            context = "\n\n".join([
                f"Q: {doc['question']}\nA: {doc['answer']}"
                for doc in context_docs[:3]
            ])
    
        # 2. Build prompt (UNCHANGED)
            skin_context = f"\n\nThe user has {skin_type} skin type." if skin_type else ""
    
            prompt = f"""You are an expert skincare assistant.

Answer the user's question using your general skincare knowledge.

USER QUESTION: {query}{skin_context}

INSTRUCTIONS:
- Be accurate and safe
- Keep response under 150 words
- Be conversational but professional

ANSWER:"""

        # 3. Generate response (UPDATED SDK CALL ONLY)
            response = self.gemini_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
    
            if response and response.text:
                return response.text.strip()
            else:
                return context_docs[0]["answer"]
    
        except Exception as e:
            print(f" Gemini generation error: {e}")
            return context_docs[0]["answer"] if context_docs else self._get_fallback(query)
    
    def get_response(self, query, skin_type=None):
        """
        Get chatbot response using RAG + Gemini
        
        Args:
            query: User's question
            skin_type: Optional skin type (Dry, Normal, Oily, etc.)
        
        Returns:
            Dict with answer, source, confidence, etc.
        """
        
        try:
            query = query.strip()
            
            # Retrieve relevant docs using FAISS
            docs = self._retrieve_relevant_docs(query, k=5)
            
            print(f"\n🔍 Query: {query}")
            if skin_type:
                print(f"👤 Skin type: {skin_type}")
            print(" Retrieved docs:")
            for i, d in enumerate(docs[:3]):
                print(f"   {i+1}. {d['question']} (score: {d['score']:.3f})")
            
            if not docs:
                return {
                    "answer": self._get_fallback(query),
                    "source": "fallback",
                    "similarity_score": 0,
                    "matched_question": None,
                    "confidence": "low"
                }
            
            best_doc = docs[0]
            best_score = best_doc["score"]
            
            # High similarity - use direct answer (fast path)
            if best_score > 0.8:
                print(f" High similarity ({best_score:.3f}) - using direct answer")
                
                return {
                    "answer": best_doc["answer"],
                    "source": "knowledge_base",
                    "similarity_score": best_score,
                    "matched_question": best_doc["question"],
                    "confidence": "high"
                }
            
            # Medium similarity - use Gemini to contextualize
            elif best_score > 0.55:
                print(f" Medium similarity ({best_score:.3f}) - using Gemini")
                
                answer = self._generate_with_gemini(query, docs, skin_type)
                
                return {
                    "answer": answer,
                    "source": "rag_gemini",
                    "similarity_score": best_score,
                    "matched_question": best_doc["question"],
                    "confidence": "medium"
                }
            
            # Low similarity - fallback
            else:
                print(f" Low similarity ({best_score:.3f}) - using Gemini (no context)")

                answer = self._generate_with_gemini(query, [], skin_type)

                return {
                    "answer": answer,
                    "source": "gemini_general",
                    "similarity_score": best_score,
                    "matched_question": best_doc["question"],
                    "confidence": "low"
                }
        
        except Exception as e:
            print(f" Chatbot error: {e}")
            import traceback
            traceback.print_exc()
            
            return {
                "answer": "I apologize, but I couldn't process your question. Could you please rephrase it?",
                "source": "error",
                "similarity_score": 0,
                "matched_question": None,
                "confidence": "low"
            }
    
    def _get_fallback(self, query):
        """Fallback response when no good match found"""
        
        q = query.lower()
        
        # Category-based fallbacks
        if any(word in q for word in ['acne', 'pimple', 'breakout', 'zit']):
            return "For acne treatment, I recommend: gentle cleanser twice daily, benzoyl peroxide 2.5-5% or salicylic acid 2%, oil-free moisturizer, and non-comedogenic products. Avoid touching your face. For severe acne, please consult a dermatologist about prescription treatments."
        
        elif any(word in q for word in ['dark circles', 'under eye', 'eye bags', 'puffy']):
            return "To reduce dark circles: get 7-8 hours of quality sleep, use caffeine or vitamin K eye cream, apply cold compress in the morning, stay hydrated (8+ glasses water daily), and always use sunscreen around eyes. For severe cases, consider consulting a dermatologist about treatments like fillers or chemical peels."
        
        elif any(word in q for word in ['wrinkle', 'fine lines', 'aging', 'anti-aging']):
            return "For anti-aging: retinol is the most effective ingredient (start 0.25-0.5%), use vitamin C serum in the morning, SPF 30+ daily (crucial!), peptides, and hyaluronic acid. Get adequate sleep, stay hydrated, don't smoke. For dramatic results, consider professional treatments like Botox or laser."
        
        elif any(word in q for word in ['dry', 'flaky', 'dehydrated', 'tight']):
            return "For dry skin: use a cream cleanser, hyaluronic acid serum on damp skin, rich moisturizer with ceramides, and hydrating sunscreen. Apply products on damp skin, use a humidifier at night, avoid hot water, and consider adding a face oil in the evening."
        
        elif any(word in q for word in ['oily', 'greasy', 'shine', 'sebum']):
            return "For oily skin: use gel or foaming cleanser, niacinamide serum (controls oil), oil-free moisturizer, and matte sunscreen. Don't over-wash as it triggers MORE oil production. Use salicylic acid 2% to unclog pores and clay masks 2x/week."
        
        elif any(word in q for word in ['routine', 'steps', 'order', 'regimen']):
            return "Basic skincare routine: MORNING - 1) Cleanser, 2) Toner (optional), 3) Serum (vitamin C), 4) Moisturizer, 5) Sunscreen SPF 30+. EVENING - 1) Cleanser, 2) Treatment (retinol 3x/week), 3) Moisturizer. Start simple and add products slowly!"
        
        elif any(word in q for word in ['sunscreen', 'spf', 'sun protection']):
            return "Sunscreen is THE most important anti-aging product! Use SPF 30+ broad spectrum daily, apply 1/4 teaspoon for face, reapply every 2 hours if outdoors. Choose mineral (zinc/titanium) for sensitive skin or chemical for no white cast. Apply EVERY day, even indoors!"
        
        else:
            return "I'd be happy to help with your skincare question! Could you ask about specific concerns like acne, dry skin, wrinkles, dark circles, routines, or specific ingredients? The more specific you are, the better I can assist you!"


# Global chatbot instance
_chatbot_instance = None


def get_chatbot():
    """Get or create global chatbot instance"""
    global _chatbot_instance
    if _chatbot_instance is None:
        _chatbot_instance = SkincareChatbot()
    return _chatbot_instance