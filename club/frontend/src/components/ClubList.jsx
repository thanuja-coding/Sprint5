import ClubItem from "./ClubItem";

function ClubList({ clubs, onApply, onToggle }) {
  return (
    <>
      <h1>Clubs</h1>
      <ul className="clubs">
        {clubs.map((club) => (
          <ClubItem key={club.id} club={club} onApply={onApply} onToggle={onToggle} />
        ))}
      </ul>
    </>
  );
}

export default ClubList;
