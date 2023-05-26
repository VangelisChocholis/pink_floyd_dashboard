track_popularity_str = '''
The popularity of a track is a value between 0 and 100, with 100 being the most popular. The popularity is calculated 
by algorithm and is based, in the most part, on the total number of plays the track has had and how recent those plays are.
'''
valence_str = '''
Valence is a measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track.
Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence 
sound more negative (e.g. sad, depressed, angry).
'''
energy_str = '''
Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity.
Typically, energetic tracks feel fast, loud, and noisy.
'''
danceability_str = '''
Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo,
rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.
'''


descr_dict = {
	'track_popularity': track_popularity_str,
	'valence': valence_str,
	'energy': energy_str,
	'danceability': danceability_str,
}