This folder is for post-processing scripts on API data.

## Scripts

- **plot_accuracy.py** plots a comparison between ADS-B truth and target localisation data in ENU coordinates.

## Docker Environment

To avoid having to install extra libraries on the host machine (e.g. numpy, matplotlib), a Dockerfile is provided to create this environment.

```bash
sudo docker build -t 3lips-script .
sudo docker run -it -v /opt/3lips/save:/app/save -v /opt/3lips/script:/app/script -v /opt/3lips/event/algorithm/geometry:/app/geometry 3lips-script bash
PYTHONPATH=/app python <script> <args>
```
