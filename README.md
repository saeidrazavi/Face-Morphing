# Face Morphing

In this repo, we implement face morphing using Delaunay Triangulation, for morphing one face into another by warping image shape and cross-dissolving image colors. 

<table>
  <tr>
    <td>brad pitt</td>
    <td>leonardo dicaprio</td>
    <td>morphing</td>

  </tr>
  <tr>
    <td><img src="https://user-images.githubusercontent.com/67091916/220162602-2faab3dd-ab63-4f47-8fee-dc6185db9106.jpg" width="350" height="250"/></td>
    <td><img src="https://user-images.githubusercontent.com/67091916/220162593-afeb6049-cd08-4e96-949b-663168e1ab5e.jpg" width="350" height="250"/></td>
    <td><img src="https://user-images.githubusercontent.com/67091916/220165335-b9993207-9124-40f3-aa49-70647d160ed4.gif" width="300" height="250"/></td>
  </tr>
 </table>

## What is face morphing?

facial morphing is the process of blending the images of two faces together. The result is a fabricated facial image that contains features of the two original faces.

## morphing

for implementation, we have to follow some essential steps:

* first align images (optional,for better quality) and resize them in order to have same size

* mark important corresponding points(eyes,ears,nose....)

* use predefined function (**`Delaunay from scipy`**) to form the triangles structure in order to warp 

* find affine transformation between triangles in the final image and two source images and apply it to final image 

## Mark important points and use Delaunay structure 

first, we mark important points contains eyes , nose, ear ....
after marking corresponding points, we save them in txt file and use them to make triangular structure using `scipy.spatial.Delaunay`
below you can see the code and result of making triangular structure :


<table>
  <tr>
    <td>triangular structure</td>
    <td>triangular structure</td>

  </tr>
  <tr>
    <td><img src="https://user-images.githubusercontent.com/67091916/220176149-9fcf5e65-7c80-4a5b-842d-bd8374174198.png" width="400" height="250"/></td>
    <td><img src="https://user-images.githubusercontent.com/67091916/220176162-e7d9fe1a-a253-4d49-978e-9f133b625a1f.png" width="400" height="250"/></td>

  </tr>
 </table>

## How to find the equivalent vertexes of triangles in the final image?

in order to find the equivalent vertexes of triangles in the final image, we use a linear transformation between vertexes of two sources. that is :

<p align="center">
  <img src="https://user-images.githubusercontent.com/67091916/220177595-6d7b12d8-f424-4bee-95b0-13afb18bb051.PNG" width="250" height="200"/>

</p>

## warping 

after making triangular structure, we have to find affine transformation matrix using **`cv2.getAffineTransform`** between each triangle and then use **`cv2.warpAffine`** to warp each triangle in the final image to corresponding triangles in the source images.
but the problem is, **how can we find all of the points that are being surrounded by 3 vertex ?!!**
to solve that problem we use a function **`cv2.fillConvexPoly`**. this function get three coordinates of triangle and fill the triangle with the desired color (with help of this function, we can label the pixels that belongs to specific triangle) . below you can see the effect of **`cv2.fillConvexPoly`** after passing 4 points to it.  


<table>
  <tr>
    <td>before fillconvex</td>
    <td>after fillconvex</td>

  </tr>
  <tr>
    <td><img src="https://user-images.githubusercontent.com/67091916/220179038-7adff63c-0723-4c44-a261-cf45b7251067.png" width="400" height="250"/></td>
    <td><img src="https://user-images.githubusercontent.com/67091916/220178948-6e4fee9a-ddcd-498b-aeaa-ce86a3303cbf.png" width="400" height="250"/></td>

  </tr>
 </table>

# Results 

<table>
  <tr>
    <td>first frame</td>
    <td>15th frame</td>
    <td>30th frame</td>
    <td>last frame </td>

  </tr>
  <tr>
    <td><img src="https://user-images.githubusercontent.com/67091916/220179915-3a60c81c-a386-457f-982e-111b4a66ffe5.jpg" width="400" height="250"/></td>
    <td><img src="https://user-images.githubusercontent.com/67091916/220179988-ee2f3aae-e9eb-4b08-a1f4-0dd4c4cd8e18.jpg" width="400" height="250"/></td>
    <td><img src="https://user-images.githubusercontent.com/67091916/220180149-fa615e0c-bf18-4503-850a-214e27aabf0a.jpg" width="400" height="250"/></td>
    <td><img src="https://user-images.githubusercontent.com/67091916/220180235-5a2b9ddd-6084-4fad-94ef-c57f313db1df.jpg" width="400" height="250"/></td>

  </tr>
 </table>

<p align="center">
  <img src="https://user-images.githubusercontent.com/67091916/220165335-b9993207-9124-40f3-aa49-70647d160ed4.gif" width="500" height="300"/>

</p>
