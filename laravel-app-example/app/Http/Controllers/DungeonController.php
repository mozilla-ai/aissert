<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;
use Illuminate\Http\JsonResponse;
use GuzzleHttp\Client;
use GuzzleHttp\Exception\RequestException;

class DungeonController extends Controller
{
    // The fixed DM instruction (same as BASE_DM_INSTRUCTION in Django)
    private $baseDMInstruction = "You are a Dungeon Master. Narrate the story based solely on the following context. Stay in character, do not add extraneous information, and follow the specified settings.\n\n";

    // Helper to build the final prompt
    private function buildPrompt(array $data): string
    {
        $worldContext   = $data['world_context'] ?? '';
        $genre          = $data['genre'] ?? '';
        $difficulty     = $data['difficulty'] ?? '';
        $narrativeTone  = $data['narrative_tone'] ?? '';
        $campaignName   = $data['campaign_name'] ?? '';
        $userQuestion   = $data['user_question'] ?? '';

        $promptBody = "World Context: {$worldContext}\n" .
                      "Genre: {$genre}\n" .
                      "Difficulty: {$difficulty}\n" .
                      "Narrative Tone: {$narrativeTone}\n" .
                      "Campaign Name: {$campaignName}\n\n" .
                      "Now, here is the player's prompt: {$userQuestion}";

        return $this->baseDMInstruction . $promptBody;
    }

    public function dungeonView(Request $request): JsonResponse
    {
        // Validate required fields
        $validatedData = $request->validate([
            'world_context'   => 'required|string',
            'genre'           => 'required|string',
            'difficulty'      => 'required|string',
            'narrative_tone'  => 'required|string',
            'campaign_name'   => 'required|string',
            'user_question'   => 'required|string',
        ]);

        // Build the final prompt
        $finalPrompt = $this->buildPrompt($validatedData);

        // Retrieve LLM settings from environment variables
        $llmProvider  = strtolower(env('LLM_PROVIDER', ''));
        $apiEndpoint  = env('LLM_API_ENDPOINT');
        $apiKey       = env('LLM_API_KEY');
        $llmModel     = env('LLM_MODEL');

        // Build the payload
        // For our purposes, we use a chat payload with a "messages" array.
        $payload = [
            "model"      => $llmModel,
            "messages"   => [
                [
                    "role"    => "system",
                    "content" => $finalPrompt
                ]
            ],
            "max_tokens" => 150,
            // Optionally add "temperature" if needed:
            "temperature" => 0.7
        ];

        // Log payload for debugging (optional)
        Log::info('LLM payload', $payload);

        try {
            // Use Guzzle to perform the HTTP POST request
            $client = new Client();
            $response = $client->post($apiEndpoint, [
                'headers' => [
                    'Authorization' => 'Bearer ' . $apiKey,
                    'Content-Type'  => 'application/json',
                ],
                'json' => $payload,
            ]);

            $responseData = json_decode($response->getBody()->getContents(), true);

            // Extract narrative from the response:
            $narrative = $responseData['choices'][0]['message']['content'] ?? '';

        } catch (RequestException $e) {
            $errorDetails = $e->hasResponse() ? $e->getResponse()->getBody()->getContents() : 'No response content';
            Log::error('LLM API error', ['error' => $e->getMessage(), 'details' => $errorDetails]);
            return response()->json([
                "error" => $e->getMessage() . ": " . $errorDetails
            ], 500);
        } catch (\Exception $e) {
            Log::error('Unexpected error', ['error' => $e->getMessage()]);
            return response()->json([
                "error" => $e->getMessage()
            ], 500);
        }

        // Return the narrative in JSON response
        return response()->json([
            "narrative" => $narrative
        ]);
    }
}
