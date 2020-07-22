# Stampify

Project to automatically convert news / entertainment websites into STAMP
(Stories on AMP) pages.

This is an internship project for Summer 2020.

Website link: [Stampify](https://stampify-279009.uc.r.appspot.com/)

<img src="https://user-images.githubusercontent.com/33183901/87937144-c6b51600-cab1-11ea-844b-41e8bc2decbd.gif" width="800">

## Demo
<table>
<tr>
<td>Original Website</td>
<td>Stampified Website</td>
</tr>
<tr>
<td><img src="https://user-images.githubusercontent.com/33183901/87933098-40e19c80-caaa-11ea-9d35-8ce5895fb4e8.gif"></td>
<td><img src="https://user-images.githubusercontent.com/33183901/87933093-3de6ac00-caaa-11ea-93a0-e8ccfe44565c.gif"></td>
</tr>
</table>

## Project Requirements

### Set Environment Variables
To get the project working, you will need to set the below mentioned API keys as environment 
variables:

- `GOOGLE_CLOUD_API_KEY` and the value as the base64 encoded string of the API key obtained from the console. For more information on creating and setting API keys, check [Using API Keys](https://cloud.google.com/docs/authentication/api-keys). To get the API key used for this project contact the owner of this repository.

### Install Dependencies
- Run the following command to install all the dependencies:

    ```
    $ pip install -r requirements.txt
    ```

    **Note:** You need pip installed in your system for running above command. To install pip, refer [official documentation](https://pip.pypa.io/en/stable/installing/).

- Run the below commands after installing the dependencies

    - Run this command in terminal:

        ```
        $ python3 -m spacy download en_core_web_sm
        ```

    - Run these commands in the python shell:

        ```
        >>> import nltk
        >>> nltk.download('punkt')
        ```

## How To Run

### Command Line Interface

#### Input:

- **url**: Url of the website to be stampified.
- **page_count**: Maximum number of stamp pages to generate.
- **-enable_animations**: Use this flag to enable animations.

#### Output:

  Generated stamp amp-html file will saved in `stampify/output/` directory.

#### Command to run:

  ```
  $ python main.py 'url' page_count(optional) -enable_animations(optional)
  ```

  Example:

    $ python main.py 'https://www.scoopwhoop.com/entertainment/memes-from-dd-ramayan/'

    $ python main.py 'https://www.scoopwhoop.com/entertainment/memes-from-dd-ramayan/' 5

    $ python main.py 'https://www.scoopwhoop.com/entertainment/memes-from-dd-ramayan/' -enable_animations

  **For more help, use command:** 
  ```python3 main.py -h```

### Flask Server

```
$ python run_server.py
```

The server will be hosted at http://0.0.0.0:8080/

#### API Endpoints:

- `GET /` to see home page for STAMPIFY
- `GET /stampified_url` to generate stamp page.
  
  **Query Params:** url, max_pages(optional), animations(optional)

### Docker Container
#### Build
```
docker build -t stampify:latest . \
    --build-arg google_cloud_api_secret="your_google_cloud_api_secret"
```

**Note:** You need docker installed in your system for running above command.

#### Run
Any port could be used from outside container. If the port you want to use is 5010, 
then run
```
docker run -d -e PORT=8080 -p 5010:8080 stampify
```

Internally, the server listens on port 8080 (This is an GCP App Engine
requirement).

#### Result
Open http://0.0.0.0:5010/

### Deploy to GCP

The following commands assume your GCP project-id is 'stampify-279009'. Your GCP
project also needs to have the container registry API enabled. GCP App Engine is
being used to run the project. Cloud Run would use similar instructions.

To deploy to GCP, first build a docker image using the instructions above.

Then you'll need to push the image to gcr.

```
docker tag stampify:latest us.gcr.io/stampify-279009/stampify:latest
docker push us.gcr.io/stampify-279009/stampify:latest
```

Verify that the image was pushed (you should be able to find it in your GCP
project images). Now to deploy the app:

```
gcloud app deploy --image-url=us.gcr.io/stampify-279009/stampify:latest
```
