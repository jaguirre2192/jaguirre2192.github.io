# Jorge Aguirre Developer Site

Static personal site built to deploy cleanly on GitHub Pages.

## Local preview

```bash
python3 -m http.server 4173
```

Then open [http://localhost:4173](http://localhost:4173).

## Publish on GitHub Pages

### Option 1: user site

1. Create a GitHub repository named `<your-github-username>.github.io`
2. Push this project to the `main` branch
3. GitHub Pages will serve it automatically at `https://<your-github-username>.github.io`

### Option 2: project site

1. Create any repo name you want
2. Push this project to the `main` branch
3. In GitHub: `Settings` -> `Pages`
4. Set `Build and deployment` to `Deploy from a branch`
5. Choose branch `main` and folder `/ (root)`

The site uses plain `index.html`, `styles.css`, and `main.js`, so there is no build step.
