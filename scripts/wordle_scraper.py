<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Today's Wordle Answer</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }

        .container {
            text-align: center;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 60px 40px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            max-width: 500px;
            width: 90%;
        }

        h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            font-weight: 700;
        }

        .subtitle {
            font-size: 1.1rem;
            opacity: 0.9;
            margin-bottom: 40px;
        }

        .answer-container {
            background: rgba(255, 255, 255, 0.15);
            border-radius: 15px;
            padding: 30px;
            margin: 30px 0;
            border: 2px solid rgba(255, 255, 255, 0.3);
        }

        .puzzle-number {
            font-size: 1rem;
            opacity: 0.8;
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .answer {
            font-size: 4rem;
            font-weight: 900;
            letter-spacing: 0.2em;
            color: #fff;
            text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            margin: 20px 0;
            text-transform: uppercase;
        }

        .date {
            font-size: 1rem;
            opacity: 0.7;
            margin-top: 15px;
        }

        .warning {
            background: rgba(255, 193, 7, 0.2);
            border: 1px solid rgba(255, 193, 7, 0.5);
            border-radius: 10px;
            padding: 20px;
            margin-top: 30px;
            font-size: 0.9rem;
            line-height: 1.5;
        }

        .loading {
            font-size: 1.2rem;
            opacity: 0.8;
        }

        .error {
            background: rgba(220, 53, 69, 0.2);
            border: 1px solid rgba(220, 53, 69, 0.5);
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
        }

        .refresh-btn {
            background: rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 8px;
            color: white;
            padding: 12px 24px;
            font-size: 1rem;
            cursor: pointer;
            margin-top: 20px;
            transition: all 0.3s ease;
        }

        .refresh-btn:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
        }

        .footer {
            margin-top: 40px;
            font-size: 0.9rem;
            opacity: 0.6;
        }

        @media (max-width: 480px) {
            .container {
                padding: 40px 20px;
            }
            
            h1 {
                font-size: 2rem;
            }
            
            .answer {
                font-size: 3rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Today's Wordle</h1>
        <p class="subtitle">Get today's answer instantly</p>
        
        <div class="answer-container">
            <div id="content">
                <div class="loading">Loading today's puzzle...</div>
            </div>
        </div>
        
        <div class="warning">
            ⚠️ <strong>Spoiler Alert!</strong> This site reveals today's Wordle answer. 
            Only visit if you want to know the solution before playing.
        </div>
        
        <button class="refresh-btn" onclick="loadWordleData()">Refresh Answer</button>
        
        <div class="footer">
            Updates automatically every day at midnight
        </div>
    </div>

    <script>
        // Store the data in memory (no localStorage in Claude artifacts)
        let currentWordleData = null;
        
        async function loadWordleData() {
            const contentDiv = document.getElementById('content');
            contentDiv.innerHTML = '<div class="loading">Loading...</div>';
            
            try {
                // Try to load from our data file
                const response = await fetch('data/wordle-data.json');
                
                if (response.ok) {
                    const data = await response.json();
                    currentWordleData = data;
                    displayWordleData(data);
                } else {
                    throw new Error('Data file not found');
                }
            } catch (error) {
                // Fallback: show example data or calculate based on date
                console.log('Using fallback data:', error);
                showFallbackData();
            }
        }
        
        function displayWordleData(data) {
            const contentDiv = document.getElementById('content');
            
            contentDiv.innerHTML = `
                <div class="puzzle-number">Wordle #${data.puzzle_number}</div>
                <div class="answer">${data.current_answer.toUpperCase()}</div>
                <div class="date">${formatDate(data.date)}</div>
            `;
        }
        
        function showFallbackData() {
            // Calculate current Wordle number based on days since launch
            const startDate = new Date('2021-06-19');
            const today = new Date();
            const daysDiff = Math.floor((today - startDate) / (1000 * 60 * 60 * 24));
            const puzzleNumber = daysDiff + 1;
            
            const contentDiv = document.getElementById('content');
            contentDiv.innerHTML = `
                <div class="puzzle-number">Wordle #${puzzleNumber}</div>
                <div class="answer">LOADING</div>
                <div class="date">${formatDate(today.toISOString().split('T')[0])}</div>
                <div class="error">
                    Unable to load today's answer. The automated system may still be updating.
                    Try refreshing in a few minutes.
                </div>
            `;
        }
        
        function formatDate(dateString) {
            const date = new Date(dateString);
            return date.toLocaleDateString('en-US', {
                weekday: 'long',
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });
        }
        
        // Load data when page loads
        loadWordleData();
        
        // Auto-refresh every 30 minutes
        setInterval(loadWordleData, 30 * 60 * 1000);
    </script>
</body>
</html>