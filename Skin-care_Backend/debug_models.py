import tensorflow as tf
import numpy as np
from PIL import Image
import sys

print("="*70)
print("COMPREHENSIVE MODEL DEBUGGING")
print("="*70)

# Load models
print("\n1. Loading models...")
model1 = tf.keras.layers.TFSMLayer('models/dermnet_densenet121_saved', call_endpoint='serving_default')
model2 = tf.keras.layers.TFSMLayer('models/dermnet_effnet_b3_saved', call_endpoint='serving_default')
print("    Models loaded")

# Load a test image (use a clear acne image)
print("\n2. Loading test image...")
try:
    img_path = sys.argv[1] if len(sys.argv) > 1 else 'test_image.jpg'
    img = Image.open(img_path).convert('RGB')
    print(f"    Image loaded: {img_path}")
    print(f"   Size: {img.size}")
except Exception as e:
    print(f"    Error: {e}")
    print("\nUsage: python debug_models.py path/to/image.jpg")
    sys.exit(1)

# Resize to 224x224
img_224 = img.resize((224, 224), Image.LANCZOS)
img_array = np.array(img_224, dtype=np.float32)

print(f"\n3. Image array info:")
print(f"   Shape: {img_array.shape}")
print(f"   Min: {img_array.min()}")
print(f"   Max: {img_array.max()}")
print(f"   Mean: {img_array.mean():.2f}")

# Class names
CLASSES = [
    'Acne', 'Actinic Keratosis', 'Atopic Dermatitis', 'Basal Cell Carcinoma',
    'Benign Keratosis', 'Cellulitis', 'Chickenpox', 'Cutaneous Larva Migrans',
    'Eczema', 'Herpes', 'Impetigo', 'Melanoma', 'Monkeypox', 'Nail Fungus',
    'Poison Ivy', 'Psoriasis', 'Ringworm', 'Rosacea', 'Scabies',
    'Seborrheic Keratoses', 'Shingles', 'Tinea', 'Warts'
]

print(f"\n4. Testing different preprocessing methods:")
print("-" * 70)

# Test 1: Raw 0-255
print("\n TEST 1: Raw values (0-255)")
img_test1 = np.expand_dims(img_array, axis=0)
tensor1 = tf.convert_to_tensor(img_test1, dtype=tf.float32)

pred1_dict = model1(tensor1)
pred2_dict = model2(tensor1)

key1 = list(pred1_dict.keys())[0]
key2 = list(pred2_dict.keys())[0]

pred1 = pred1_dict[key1].numpy()[0]
pred2 = pred2_dict[key2].numpy()[0]

print(f"   Model 1 (DenseNet):")
print(f"      Top class: {CLASSES[np.argmax(pred1)]} ({pred1.max()*100:.2f}%)")
print(f"      Top 3: ", end="")
top3 = np.argsort(pred1)[-3:][::-1]
for idx in top3:
    print(f"{CLASSES[idx]}({pred1[idx]*100:.1f}%) ", end="")
print()

print(f"   Model 2 (EfficientNet):")
print(f"      Top class: {CLASSES[np.argmax(pred2)]} ({pred2.max()*100:.2f}%)")
print(f"      Top 3: ", end="")
top3 = np.argsort(pred2)[-3:][::-1]
for idx in top3:
    print(f"{CLASSES[idx]}({pred2[idx]*100:.1f}%) ", end="")
print()

# Test 2: Normalized 0-1
print("\n📊 TEST 2: Normalized (0-1)")
img_test2 = img_array / 255.0
img_test2 = np.expand_dims(img_test2, axis=0)
tensor2 = tf.convert_to_tensor(img_test2, dtype=tf.float32)

pred1_dict = model1(tensor2)
pred2_dict = model2(tensor2)

pred1 = pred1_dict[key1].numpy()[0]
pred2 = pred2_dict[key2].numpy()[0]

print(f"   Model 1 (DenseNet):")
print(f"      Top class: {CLASSES[np.argmax(pred1)]} ({pred1.max()*100:.2f}%)")
print(f"   Model 2 (EfficientNet):")
print(f"      Top class: {CLASSES[np.argmax(pred2)]} ({pred2.max()*100:.2f}%)")

# Test 3: ImageNet normalization
print("\n TEST 3: ImageNet normalization")
img_test3 = img_array / 255.0
mean = np.array([0.485, 0.456, 0.406])
std = np.array([0.229, 0.224, 0.225])
img_test3 = (img_test3 - mean) / std
img_test3 = np.expand_dims(img_test3, axis=0)
tensor3 = tf.convert_to_tensor(img_test3, dtype=tf.float32)

pred1_dict = model1(tensor3)
pred2_dict = model2(tensor3)

pred1 = pred1_dict[key1].numpy()[0]
pred2 = pred2_dict[key2].numpy()[0]

print(f"   Model 1 (DenseNet):")
print(f"      Top class: {CLASSES[np.argmax(pred1)]} ({pred1.max()*100:.2f}%)")
print(f"   Model 2 (EfficientNet):")
print(f"      Top class: {CLASSES[np.argmax(pred2)]} ({pred2.max()*100:.2f}%)")

# Test 4: DenseNet specific (Caffe mode)
print("\n TEST 4: DenseNet Caffe mode (BGR, mean subtraction)")
img_test4 = img_array.copy()
# RGB to BGR
img_test4 = img_test4[..., ::-1]
# Mean subtraction
mean = [103.939, 116.779, 123.68]
img_test4[..., 0] -= mean[0]
img_test4[..., 1] -= mean[1]
img_test4[..., 2] -= mean[2]
img_test4 = np.expand_dims(img_test4, axis=0)
tensor4 = tf.convert_to_tensor(img_test4, dtype=tf.float32)

pred1_dict = model1(tensor4)
pred1 = pred1_dict[key1].numpy()[0]

print(f"   Model 1 (DenseNet):")
print(f"      Top class: {CLASSES[np.argmax(pred1)]} ({pred1.max()*100:.2f}%)")
print(f"      Top 3: ", end="")
top3 = np.argsort(pred1)[-3:][::-1]
for idx in top3:
    print(f"{CLASSES[idx]}({pred1[idx]*100:.1f}%) ", end="")
print()

print("\n" + "="*70)
print(" TESTING COMPLETE")
print("="*70)
print("\nLook for the test that gives:")
print("  1. HIGH confidence (>80%)")
print("  2. CORRECT prediction")
print("  3. Both models AGREE")
print("\nThat's the correct preprocessing method!")